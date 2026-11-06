#!/usr/bin/env python3
"""Decode video and extract paginated samples and critical strips; subjective reviews stay pending."""
import argparse,json,math,subprocess
from fractions import Fraction
from pathlib import Path
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('video',type=Path)
    p.add_argument('--output-dir',required=True,type=Path);p.add_argument('--samples',type=int,default=8)
    p.add_argument('--beats',type=Path);p.add_argument('--times',default='')
    p.add_argument('--strip',type=float,action='append',default=[]);p.add_argument('--timeline-start',type=float,default=0)
    a=p.parse_args()
    if not a.video.is_file() or not 2<=a.samples<=60 or not math.isfinite(a.timeline_start) or a.timeline_start<0:p.error('Invalid file, samples or timeline origin')
    a.output_dir.mkdir(parents=True,exist_ok=True)
    data=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(a.video)]).stdout)
    v=next((s for s in data['streams'] if s.get('codec_type')=='video'),None)
    if v is None:raise ValueError('No video stream')
    duration=float(v.get('duration') or data['format']['duration']);fps=float(Fraction(v['avg_frame_rate']))
    if duration<=0 or fps<=0:raise ValueError('Invalid duration/FPS')
    count=int(v['nb_read_frames']) if str(v.get('nb_read_frames','')).isdigit() else math.ceil(duration*fps)
    decoded=run(['ffmpeg','-v','error','-i',str(a.video),'-f','null','-'])
    if decoded.stderr.strip():raise ValueError(decoded.stderr[-4000:])
    main_ids={round((count-1)*i/(a.samples-1)) for i in range(a.samples)}
    times=[float(t) for t in a.times.split(',') if t.strip()]
    if any(not math.isfinite(t) for t in times+a.strip):p.error('Non-finite sample time')
    if a.beats:
        grid=json.loads(a.beats.read_text());times.extend(grid['beats'])
    for t in times:
        if not isinstance(t,(float,int)) or not math.isfinite(t):p.error('Invalid beat time')
        local=t-a.timeline_start
        if 0<=local<duration:main_ids.add(min(count-1,round(local*fps)))
    strips=[]
    for t in a.strip:
        local=t-a.timeline_start
        if not 0<=local<duration:p.error('Strip time outside exported interval')
        center=round(local*fps);ids=list(range(max(0,center-6),min(count,center+6)));strips.append((t,ids))
    ids=sorted(main_ids.union(*(set(s[1]) for s in strips)))
    if len(ids)>600:p.error('More than 600 samples: inspect smaller intervals')
    expr='+'.join(f'eq(n\\,{n})' for n in ids)
    run(['ffmpeg','-v','error','-y','-i',str(a.video),'-vf',f'select={expr},scale=360:-2','-fps_mode','vfr',str(a.output_dir/'sample-%04d.png')])
    samples={}
    for i,n in enumerate(ids):
        f=a.output_dir/f'sample-{i+1:04d}.png'
        if not f.is_file():raise ValueError(f'Missing sample for frame {n}')
        samples[n]={'frame':n,'time':round(n/fps,6),'timeline_time':round(a.timeline_start+n/fps,6),'file':str(f.resolve())}
    from PIL import Image,ImageDraw
    with Image.open(samples[ids[0]]['file']) as im:w,h=im.size
    def sheet(batch,name,cols):
        out=Image.new('RGB',(cols*w,math.ceil(len(batch)/cols)*(h+28)),'#ececec');d=ImageDraw.Draw(out)
        for j,n in enumerate(batch):
            x=(j%cols)*w;y=(j//cols)*(h+28)
            with Image.open(samples[n]['file']) as im:out.paste(im.convert('RGB'),(x,y))
            d.text((x+5,y+h+5),f"{samples[n]['timeline_time']:.3f}s",fill='black')
        f=a.output_dir/name;out.save(f,quality=90);return str(f.resolve())
    ordered=sorted(main_ids);contacts=[]
    for i in range(0,len(ordered),24):contacts.append(sheet(ordered[i:i+24],f'contact-{i//24+1:02d}.jpg',4))
    strip_files=[{'time':t,'file':sheet(ns,f'strip-{i+1:02d}.jpg',4)} for i,(t,ns) in enumerate(strips)]
    report={'video':str(a.video.resolve()),'duration':duration,'width':v['width'],'height':v['height'],'fps':fps,'frames':count,
            'timeline_start':a.timeline_start,'has_audio':any(s.get('codec_type')=='audio' for s in data['streams']),
            'full_decode_check':'passed','samples':[samples[n] for n in ids],'contact_sheets':contacts,'strips':strip_files,
            'visual_review':'pending','motion_playback_review':'pending','listening_review':'pending'}
    (a.output_dir/'inspection.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='samples'}))
if __name__=='__main__':main()

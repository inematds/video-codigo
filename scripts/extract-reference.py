#!/usr/bin/env python3
"""Sample a local reference video, with paginated contact sheets and explicit coverage."""
import argparse,json,math,subprocess
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('video',type=Path)
    p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--interval',type=float,default=.5)
    p.add_argument('--start',type=float,default=0);p.add_argument('--end',type=float)
    p.add_argument('--max-frames',type=int,default=240);a=p.parse_args()
    if not a.video.is_file():p.error('Video does not exist')
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(a.video)]))
    duration=float(data['format']['duration']);end=duration if a.end is None else a.end
    if not all(math.isfinite(v) for v in [a.start,end,a.interval]) or not 0<=a.start<end<=duration or a.interval<=0 or not 1<=a.max_frames<=1000:p.error('Invalid interval, range or max-frames')
    total=math.ceil((end-a.start)/a.interval);count=min(a.max_frames,total)
    a.output_dir.mkdir(parents=True,exist_ok=True)
    frames=[]
    for i in range(count):
        t=a.start+i*a.interval;f=a.output_dir/f'ref-{i:04d}.jpg'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(a.video),'-frames:v','1','-vf','scale=360:-2','-q:v','2',str(f)],check=True)
        if not f.is_file():raise ValueError(f'Missing frame at {t}')
        frames.append({'time':round(t,6),'file':str(f.resolve())})
    from PIL import Image,ImageDraw
    with Image.open(frames[0]['file']) as im:w,h=im.size
    sheets=[]
    for page in range(math.ceil(count/24)):
        batch=frames[page*24:(page+1)*24];sheet=Image.new('RGB',(w*4,(h+28)*math.ceil(len(batch)/4)),'#efefef');d=ImageDraw.Draw(sheet)
        for j,item in enumerate(batch):
            with Image.open(item['file']) as im:sheet.paste(im.convert('RGB'),((j%4)*w,(j//4)*(h+28)))
            d.text(((j%4)*w+6,(j//4)*(h+28)+h+5),f"{item['time']:.3f}s",fill='black')
        f=a.output_dir/f'contact-{page+1:02d}.jpg';sheet.save(f,quality=90);sheets.append(str(f.resolve()))
    report=dict(video=str(a.video.resolve()),duration=duration,requested_range=[a.start,end],interval=a.interval,
                coverage_complete=count==total,last_sample_time=frames[-1]['time'],frames=frames,contact_sheets=sheets,
                visual_observation='pending',playback='pending',listening='pending')
    (a.output_dir/'reference.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({'frames':count,'requested_frames':total,'coverage_complete':count==total,'contact_sheets':sheets}))
if __name__=='__main__':main()

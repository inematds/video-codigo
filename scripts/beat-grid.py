#!/usr/bin/env python3
"""Create a known-tempo grid or estimate beats from audio without inventing meter phase."""
import argparse,json,math,subprocess,tempfile
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    source=p.add_mutually_exclusive_group(required=True)
    source.add_argument('--bpm',type=float);source.add_argument('--audio',type=Path)
    p.add_argument('--duration',type=float);p.add_argument('--offset',type=float,default=0)
    p.add_argument('--meter',type=int,default=4);p.add_argument('--downbeat-index',type=int)
    p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    if a.meter<1 or not math.isfinite(a.offset) or a.offset<0:p.error('Invalid meter/offset')
    if a.downbeat_index is not None and not 0<=a.downbeat_index<a.meter:p.error('downbeat-index must be within the meter')
    if a.bpm is not None:
        if not math.isfinite(a.bpm) or a.bpm<=0 or a.duration is None or not math.isfinite(a.duration) or a.duration<=0 or a.offset>=a.duration:p.error('Known grid needs positive BPM/duration and offset within duration')
        bpm=a.bpm;duration=a.duration;step=60/bpm
        beats=[a.offset+i*step for i in range(math.ceil((duration-a.offset)/step)) if a.offset+i*step<duration]
        phase=0 if a.downbeat_index is None else a.downbeat_index
        method='declared_tempo';hits=[];phase_status='declared';source_file=None
    else:
        if not a.audio.is_file():p.error('Audio does not exist')
        if a.offset or a.duration is not None:p.error('Audio analysis uses the complete file; do not force duration/offset')
        try:import numpy as np;import librosa
        except ImportError:p.error('Audio analysis requires numpy and librosa')
        with tempfile.TemporaryDirectory(prefix='beat-analysis-') as tmp:
            wav=Path(tmp)/'analysis.wav'
            subprocess.run(['ffmpeg','-v','error','-y','-i',str(a.audio),'-vn','-ac','1','-ar','22050',str(wav)],check=True)
            y,sr=librosa.load(wav,sr=None);duration=len(y)/sr
            if not len(y) or float(np.max(np.abs(y)))<1e-5:p.error('No useful audio signal')
            onset=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
            tempo,frames=librosa.beat.beat_track(onset_envelope=onset,sr=sr,hop_length=256,trim=False)
            beats=librosa.frames_to_time(frames,sr=sr,hop_length=256).tolist()
            hit_frames=librosa.onset.onset_detect(onset_envelope=onset,sr=sr,hop_length=256,units='frames')
            hits=librosa.frames_to_time(hit_frames,sr=sr,hop_length=256).tolist()
            bpm=float(np.atleast_1d(tempo)[0])
        if not math.isfinite(bpm) or bpm<=0 or not beats:p.error('Beat estimate unavailable; mark beats manually')
        beats=[t for t in beats if 0<=t<duration];hits=[t for t in hits if 0<=t<duration]
        phase=a.downbeat_index;phase_status='unverified' if phase is None else 'declared'
        method='estimated_from_audio';source_file=str(a.audio.resolve())
    result=dict(schema_version=1,method=method,audio=source_file,duration=duration,bpm=bpm,meter=a.meter,
                beats=[round(t,6) for t in beats],downbeats=[] if phase is None else [round(t,6) for t in beats[phase::a.meter]],
                hits=[round(t,6) for t in hits],downbeat_phase=phase_status,listening_verified=False)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2))
    print(json.dumps({'output':str(a.output.resolve()),'method':method,'bpm':bpm,'beats':len(beats),'downbeat_phase':phase_status}))
if __name__=='__main__':main()

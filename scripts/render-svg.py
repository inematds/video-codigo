#!/usr/bin/env python3
"""Render time-indexed SVG from an authored Python module, without a browser."""
import argparse
import importlib.util
import json
import math
import subprocess
import tempfile
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scene', type=Path, required=True, help='Módulo propio con VIDEO_SPEC y frame(t,width,height) -> SVG')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--width', type=int)
    p.add_argument('--height', type=int)
    p.add_argument('--fps', type=int)
    p.add_argument('--duration', type=float)
    p.add_argument('--still', type=float)
    p.add_argument('--audio', type=Path)
    p.add_argument('--start', type=float, default=0)
    p.add_argument('--end', type=float)
    p.add_argument('--subframes', type=int, choices=[1,2,4,8], default=1)
    p.add_argument('--shutter', type=float, default=.5)
    p.add_argument('--overwrite', action='store_true')
    a = p.parse_args()
    if a.output.exists() and not a.overwrite:
        p.error('La exportación existe; usar otro nombre o --overwrite')
    if a.output.suffix.lower() != ('.png' if a.still is not None else '.mp4'):
        p.error('Usar PNG para --still y MP4 para vídeo')
    if a.audio and (not a.audio.is_file() or a.still is not None):
        p.error('Audio debe ser un archivo existente y usarse en modo vídeo')
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('video_scene', a.scene.resolve())
    scene = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scene)
    values = {k: getattr(a, k) if getattr(a, k) is not None else scene.VIDEO_SPEC[k]
              for k in ['width', 'height', 'fps', 'duration']}
    w, h, fps, duration = (values[k] for k in ['width', 'height', 'fps', 'duration'])
    if not all(isinstance(n, int) and n > 0 and n % 2 == 0 for n in [w, h]):
        p.error('Dimensiones positivas pares')
    if not isinstance(fps, int) or not 1 <= fps <= 120 or not math.isfinite(duration) or duration <= 0:
        p.error('FPS entre 1 y 120; duración positiva')
    import cairosvg
    def frame(t):
        svg = scene.frame(t, w, h)
        # Only inline resources in authored SVG, so rendering needs no remote requests.
        import re
        for ref in re.findall(r'(?:href\s*=\s*[\"\']([^\"\']+)|url\(\s*([^)]*))', svg):
            target = next(x for x in ref if x).strip(' \"\'')
            if not target.startswith(('#', 'data:')):
                raise ValueError('SVG debe usar recursos inline: ' + target)
        return cairosvg.svg2png(bytestring=svg.encode('utf-8'), output_width=w, output_height=h, unsafe=False)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.still is not None:
        if not 0 <= a.still < duration:
            p.error('--still fuera de duración')
        a.output.write_bytes(frame(a.still))
        print(json.dumps({'output': str(a.output), 'time': a.still, 'width': w, 'height': h}))
        return
    start, end = a.start, duration if a.end is None else a.end
    if not all(math.isfinite(n) for n in [start,end,a.shutter]) or not 0 <= start < end <= duration or not 0 <= a.shutter <= 1:
        p.error('Intervalo o shutter inválidos')
    count = math.ceil((end-start) * fps)
    actual = count / fps
    t = start + (end-start)*.37
    before = frame(t)
    frame(duration * .73)
    if before != frame(t):
        raise ValueError('frame(t) no es determinista')
    with tempfile.TemporaryDirectory(prefix='svg-video-') as tmp:
        for i in range(count):
            target = Path(tmp) / f'frame-{i:06d}.png'
            if a.subframes == 1:
                target.write_bytes(frame(min(duration-1e-9,start+i/fps)))
            else:
                from PIL import Image
                from io import BytesIO
                blended = None
                for j in range(a.subframes):
                    sample = max(0,min(duration-1e-9,start+i/fps+((j+.5)/a.subframes-.5)*a.shutter/fps))
                    im = Image.open(BytesIO(frame(sample))).convert('RGB')
                    blended = im if blended is None else Image.blend(blended,im,1/(j+1))
                blended.save(target)
        cmd = ['ffmpeg', '-v', 'error', '-y' if a.overwrite else '-n', '-framerate', str(fps),
               '-i', str(Path(tmp) / 'frame-%06d.png')]
        if a.audio:
            cmd += ['-ss', str(start), '-i', str(a.audio.resolve()), '-map', '0:v:0', '-map', '1:a:0',
                    '-af', 'apad', '-c:a', 'aac', '-b:a', '192k']
        else:
            cmd += ['-an']
        cmd += ['-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-t', str(actual),
                '-movflags', '+faststart', str(a.output.resolve())]
        subprocess.run(cmd, check=True)
    report = {'output': str(a.output.resolve()), **values, 'requested_duration': end-start, 'source_start': start, 'source_end': end,
              'subframes': a.subframes, 'shutter': a.shutter,
              'duration': actual, 'frames': count, 'audio': bool(a.audio), 'deterministic_seek_check': True}
    Path(str(a.output) + '.render.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()

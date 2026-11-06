#!/usr/bin/env bash
# MP4 largo sin llenar el disco: renderiza por tramos (cada tramo guarda sus fotogramas en temporal, ~100 KB por
# fotograma a 1080p, los codifica y los borra), los une sin recodificar y pone el audio con un limitador de picos.
#   bash render-tramos.sh PROYECTO ENTRADA.html SALIDA.mp4 DURACION [AUDIO.wav] [FPS=30] [TRAMO=60]
# DURACION = window.videoSpec.duration de la página. Si un tramo falla, se relanza el mismo comando: los tramos
# ya hechos no se repiten. El 29-oct-2026 un render de 9 min de una sola vez llenó el disco: por eso existe.
set -euo pipefail
PROY="$(cd "$1" && pwd)"; ENTRADA="$2"; SALIDA="$3"; DUR="$4"; AUDIO="${5:-}"; FPS="${6:-30}"; TRAMO="${7:-60}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
TMP="$(cd "$(dirname "$SALIDA")" && pwd)/.tramos-$(basename "$SALIDA" .mp4)"
mkdir -p "$TMP"
: > "$TMP/lista.txt"
python3 -c "
import math
d=float('$DUR'); t=float('$TRAMO')
for i in range(math.ceil(d/t-1e-9)): print(i, i*t, min(d,(i+1)*t))" | while read -r N A B; do
  F="$TMP/$(printf '%03d' "$N").mp4"
  [ -f "$F" ] || node "$AQUI/render-video.mjs" --project "$PROY" --entry "$ENTRADA" --output "$F" --fps "$FPS" --start "$A" --end "$B" --overwrite > /dev/null
  echo "file '$(basename "$F")'" >> "$TMP/lista.txt"
  echo "tramo $N ($A-$B s) listo"
done
if [ -n "$AUDIO" ]; then
  ffmpeg -loglevel error -y -f concat -safe 0 -i "$TMP/lista.txt" -c copy "$TMP/video.mp4"
  ffmpeg -loglevel error -y -i "$TMP/video.mp4" -i "$AUDIO" -map 0:v -map 1:a -c:v copy \
    -af "alimiter=limit=0.79:level=false" -c:a aac -b:a 192k -shortest "$SALIDA"
else
  ffmpeg -loglevel error -y -f concat -safe 0 -i "$TMP/lista.txt" -c copy "$SALIDA"
fi
rm -r "$TMP"
echo "Listo: $SALIDA"

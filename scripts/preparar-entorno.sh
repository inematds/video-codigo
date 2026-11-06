#!/usr/bin/env bash
# Comprueba e instala lo necesario para renderizar: Node, FFmpeg, Python con Pillow
# y Playwright con Chromium. Playwright va a ~/.cache/crear-videos-con-codigo, donde
# render-video.mjs lo encuentra solo. No toca el sistema ni instala nada con sudo.
#
# Uso:  bash scripts/preparar-entorno.sh              comprobar e instalar Playwright
#       bash scripts/preparar-entorno.sh --comprobar  solo comprobar, sin instalar
set -uo pipefail

DIR="${CVC_DEPS_DIR:-$HOME/.cache/crear-videos-con-codigo}"
PLAYWRIGHT_VERSION="1.62.1"
SOLO_COMPROBAR=0
[ "${1:-}" = "--comprobar" ] && SOLO_COMPROBAR=1
FALTA=0

ok()    { printf '  ✓ %s\n' "$1"; }
falta() { printf '  ✗ %s\n    → %s\n' "$1" "$2"; FALTA=1; }

echo "Comprobando dependencias de crear-videos-con-codigo…"

if command -v node >/dev/null 2>&1; then
  MAYOR=$(node -p 'process.versions.node.split(".")[0]')
  if [ "$MAYOR" -ge 18 ]; then ok "Node $(node -v)"; else falta "Node $(node -v) es antiguo" "instala Node 18 o superior desde https://nodejs.org"; fi
else
  falta "Node no está instalado" "instálalo desde https://nodejs.org (versión LTS)"
fi

if command -v ffmpeg >/dev/null 2>&1; then
  ok "FFmpeg $(ffmpeg -version | head -1 | awk '{print $3}')"
else
  falta "FFmpeg no está instalado" "Mac: brew install ffmpeg · Windows: winget install ffmpeg · Linux: sudo apt install ffmpeg"
fi

if command -v python3 >/dev/null 2>&1; then
  ok "Python $(python3 -c 'import platform; print(platform.python_version())')"
  if python3 -c 'import numpy' >/dev/null 2>&1; then ok "numpy (voz e mixagem)"; else falta "Falta numpy" "python3 -m pip install --user numpy"; fi
  if python3 -c 'import PIL' >/dev/null 2>&1; then ok "Pillow (hojas de revisión)"; else falta "Falta Pillow" "python3 -m pip install --user pillow"; fi
  if python3 -c 'import librosa' >/dev/null 2>&1; then ok "librosa (detectar pulsos de una canción)"; else echo "  · librosa no está: opcional, solo para analizar una pista existente (python3 -m pip install --user librosa)"; fi
  if python3 -c 'import cairosvg' >/dev/null 2>&1; then ok "CairoSVG (ruta SVG)"; else echo "  · CairoSVG no está: opcional, solo para la ruta SVG (python3 -m pip install --user cairosvg)"; fi
else
  falta "Python 3 no está instalado" "instálalo desde https://www.python.org"
fi

if [ -d "$DIR/node_modules/playwright" ]; then
  ok "Playwright en $DIR"
elif [ "$SOLO_COMPROBAR" -eq 1 ]; then
  falta "Playwright no está preparado" "ejecuta este script sin --comprobar"
elif command -v npm >/dev/null 2>&1; then
  echo "  Instalando Playwright $PLAYWRIGHT_VERSION en $DIR…"
  mkdir -p "$DIR"
  if [ ! -f "$DIR/package.json" ]; then
    printf '{"name":"crear-videos-con-codigo-deps","private":true}\n' > "$DIR/package.json"
  fi
  if (cd "$DIR" && npm install --silent --no-audit --no-fund "playwright@$PLAYWRIGHT_VERSION"); then
    ok "Playwright $PLAYWRIGHT_VERSION instalado"
  else
    falta "No se pudo instalar Playwright" "revisa la conexión y vuelve a ejecutar el script"
  fi
else
  falta "npm no está disponible" "viene con Node: reinstala Node desde https://nodejs.org"
fi

if [ -n "${VIDEO_CHROMIUM_PATH:-}" ]; then
  if [ -x "$VIDEO_CHROMIUM_PATH" ]; then ok "Navegador de render: $VIDEO_CHROMIUM_PATH"; else falta "VIDEO_CHROMIUM_PATH no apunta a un ejecutable" "corrige la ruta o quita la variable"; fi
elif [ -d "$DIR/node_modules/playwright" ]; then
  if (cd "$DIR" && node -e 'const fs=require("fs");const {chromium}=require("playwright");process.exit(fs.existsSync(chromium.executablePath())?0:1)' 2>/dev/null); then
    ok "Chromium de Playwright"
  elif [ "$SOLO_COMPROBAR" -eq 1 ]; then
    falta "Falta el Chromium de Playwright" "ejecuta este script sin --comprobar"
  else
    echo "  Descargando Chromium para Playwright (unos 150 MB, solo la primera vez)…"
    if (cd "$DIR" && npx --no-install playwright install chromium >/dev/null); then ok "Chromium listo"; else falta "No se pudo descargar Chromium" "vuelve a ejecutar el script o define VIDEO_CHROMIUM_PATH con la ruta de tu Chrome"; fi
  fi
fi

echo
if [ "$FALTA" -eq 0 ]; then
  echo "Todo listo. Prueba: node \"$(cd "$(dirname "$0")" && pwd)/render-video.mjs\" --help"
else
  echo "Falta algo (marcado con ✗). Instálalo y vuelve a ejecutar este script."
  exit 1
fi

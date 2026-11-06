# 🎬 video-codigo — vídeos hechos con código

[![Vídeo con código](guia/assets/banner-es.jpg)](https://inematds.github.io/video-codigo/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

video-codigo es una skill para Claude Code (y Codex) que crea vídeos sin cámara ni editor: cada fotograma se escribe en código (HTML, Canvas o SVG) y se convierte en MP4. Sirve para quienes quieren mostrar un producto, un proyecto o una idea en vídeo: un lanzamiento, un anuncio, un explicativo, una serie de productos o una clase. Si el vídeo lleva narración, la voz se genera en tu computadora (sin pagar por la voz) y cada imagen aparece en el instante en que se pronuncia la palabra. Necesita Node, Python, FFmpeg y, para la voz, inemavox con una GPU NVIDIA (sin ella, el vídeo se genera solo con música).

## 📖 Guía de uso

Guía completa (landing + paso a paso + ejemplos): **https://inematds.github.io/video-codigo/guia/es/**

## Lo que hace

- **Tres preguntas antes de empezar:** de qué trata y para quién es; con voz o solo con música; qué estilo.
- **Lee la fuente:** documento, carpeta, repositorio o sitio web: «léelo todo y propónme un vídeo».
- **Voz local sincronizada:** `scripts/voz.py` genera la narración con la voz clonada (Chatterbox) y mide el tiempo de cada palabra (Whisper); el motor `assets/voz-sync/` sincroniza cada imagen con una palabra (`pal('frase', 'palabra')`).
- **Música original sintetizada:** `scripts/mezcla.py` (120 o 84 BPM), a volumen bajo bajo la voz.
- **16:9 y 9:16 del mismo proyecto:** el diseño se recalcula según el formato.
- **Vista previa antes de renderizar el vídeo completo** y revisión del MP4 con hojas de fotogramas (`scripts/inspect-video.py`).
- **Tema INEMA listo:** `assets/inema/` (colores, fuentes locales, subtítulos con contorno).

## El proceso, de principio a fin

Quién se encarga: 🧠 sesión contigo · ⚙️ script · 🤖 agente (Claude Code siguiendo `SKILL.md`). En los comandos, `P` es la carpeta del vídeo (p. ej., `~/videos/trabalho/2026-11-06-meuapp`) y `scripts/` es la del kit (ejecútalos desde `~/projetos/video-codigo` o usa la ruta completa).

| # | Paso | Comando / acción | Quién |
|---|---|---|---|
| 1 | Pedir el vídeo | "/video-codigo crea un vídeo de 40 s de mi producto, lee la carpeta X" | 🧠 |
| 2 | Responder las 3 preguntas | tema y público · con voz o solo con música · estilo (INEMA predeterminado o una referencia) | 🧠 |
| 3 | Leer la fuente y proponer una dirección | brief, guion de planos, duración y formatos | 🤖 |
| 4 | Aprobar la propuesta (si quieres aprobarla) | el agente muestra la propuesta; una orden explícita de producir ya es suficiente | 🧠 |
| 5 | Guion → voz con tiempos por palabra | `python3 scripts/voz.py --projeto P P/roteiro.json` → `voz.wav`, `tiempos.js` | ⚙️ |
| 6 | Música y mezcla | `python3 scripts/mezcla.py --projeto P --id <id> --musica tranquila --lufs -14` | ⚙️ |
| 7 | Escribir las escenas | partir de `exemplos/explicativo-narrado/` (con voz) o `exemplos/lancamento/` (solo música) y cambiar las escenas | 🤖 |
| 8 | Vista previa: fotogramas sueltos y un fragmento | `node scripts/render-video.mjs --project P --output prova.png --still 3` (y `--start/--end`) | ⚙️ + 🤖 |
| 9 | Renderizar en 16:9 y 9:16 | `node scripts/render-video.mjs --project P --output P/renders/x.mp4 --audio P/audio/<id>/mezcla.wav` (+ `--width 1080 --height 1920`) | ⚙️ |
| 10 | Revisión | `python3 scripts/inspect-video.py P/renders/x.mp4 --output-dir P/reviews` y revisar las hojas | ⚙️ + 🤖 |
| 11 | Entrega | MP4 + portada + proyecto editable; publicar solo con tu aprobación | 🧠 |

## Instalación

```bash
git clone https://github.com/inematds/video-codigo ~/projetos/video-codigo
bash ~/projetos/video-codigo/instalar.sh     # conecta la skill con Claude Code/Codex e instala Playwright (sin sudo)
```

Requisitos previos: Node 18+, Python 3 con `numpy`, `scipy` y Pillow, FFmpeg. `instalar.sh` instala Playwright y Chromium (sin sudo); comprueba el resto y muestra el comando correspondiente. **Voz (opcional):** [inemavox](https://github.com/inematds/inemavox) en `~/projetos/inemavox`, con el entorno Chatterbox (`~/miniconda3/envs/chatterbox`) y Whisper en su `venv`; la voz de referencia es un archivo `.wav` de 10–20 s (`"voz": "/caminho/minha-voz.wav"` en el guion). Sin voz, la skill funciona solo con música.

```bash
# voz local (probado: Python 3.11, chatterbox-tts 0.1.6, GPU NVIDIA, Miniconda; los modelos descargan varios GB en el primer uso)
# conda o inemavox en otra ubicación: CHATTERBOX_PYTHON=/caminho/python3  INEMAVOX_DIR=/caminho/inemavox
git clone https://github.com/inematds/inemavox ~/projetos/inemavox
conda create -n chatterbox python=3.11 -y
~/miniconda3/envs/chatterbox/bin/pip install chatterbox-tts==0.1.6
cd ~/projetos/inemavox && python3 -m venv venv && venv/bin/pip install faster-whisper soundfile numpy
```

Prueba rápida de la instalación (sin voz, ~1 min):
`cd ~/projetos/video-codigo/exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output teste.mp4 --audio audio/lancamento/mezcla.wav --overwrite`

## Ejemplos (hechos con el propio kit)

| Ejemplo | Tipo | Archivos |
|---|---|---|
| Este vídeo no tiene cámara | explicativo narrado (voz local), 44 s | `exemplos/explicativo-narrado/` · `renders/explicativo-16x9.mp4` · `renders/explicativo-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=tkT2I6nrMAk) |
| INEMA.CLUB en un plano | lanzamiento solo con música, 21 s | `exemplos/lancamento/` · `renders/lancamento-16x9.mp4` · `renders/lancamento-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=IJ-qZQ1drBc) |

El guion del ejemplo narrado usa la voz `nei`, que solo existe en la computadora del autor: para volver a generar la voz, ejecútalo con `VC_VOZ=/caminho/sua-voz.wav`. Para rehacer solo el vídeo (el audio ya está en el repositorio): `cd exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output x.mp4 --audio audio/lancamento/mezcla.wav`.

## Estructura

```
SKILL.md              instrucciones de la skill (el agente sigue esto)
references/           brief, dirección, movimiento, sonido, voz, renderizado, revisión, prompts de película
scripts/              voz.py (voz local) · mezcla.py · render-video.mjs · render-tramos.sh · inspect-video.py · …
assets/inema/         tema INEMA + fuentes locales
assets/voz-sync/      motor de tiempos (imagen sincronizada con la palabra)
exemplos/ renders/    dos vídeos completos y los MP4
guia/                 página de la guía (PT/EN/ES)
```

---
[INEMA.CLUB](https://inema.club)
# 🎬 video-codigo — vídeos hechos con código

[![Vídeo con código](guia/assets/banner-es.jpg)](https://inematds.github.io/video-codigo/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

video-codigo es una skill para Claude Code (y Codex) que crea vídeos sin cámara ni editor: cada fotograma se escribe
en código (HTML, Canvas o SVG) y se convierte en MP4. Sirve para quienes quieren presentar un producto, un proyecto o una idea
en vídeo: lanzamiento, anuncio, explicativo, serie de productos o clase. Si el vídeo lleva narración, la voz se genera en tu
computadora (sin pagar por la voz) y cada imagen aparece en el instante en que se pronuncia la palabra. Necesita Node, Python, FFmpeg y,
para la voz, inemavox con GPU NVIDIA (sin ella, el vídeo se genera solo con música).

## 📖 Guía de uso

Guía completa (landing + paso a paso + ejemplos): **https://inematds.github.io/video-codigo/guia/es/**

## Qué hace

- **Tres preguntas antes de empezar:** de qué trata y para quién; con voz o solo con música; qué estilo.
- **Lee la fuente:** documento, carpeta, repositorio o sitio — «lee todo y me propone un video».
- **Voz local sincronizada:** `scripts/voz.py` genera la narración con la voz clonada (Chatterbox) y mide el tiempo de cada
  palabra (Whisper); el motor `assets/voz-sync/` vincula cada imagen a una palabra (`pal('frase', 'palavra')`).
- **Voz verificada por Whisper:** cada frase se vuelve a escuchar y se rehace si no coincide (similitud o número incorrecto);
  todo queda en `voz/<id>/checagem.md`, con lo que oyó Whisper. `scripts/checar-fala.py` lo verifica después.
- **Música original sintetizada y ajustada a los cortes:** `scripts/mezcla.py` (120 o 84 BPM), muy baja debajo de la voz;
  cada corte de escena cae en un tiempo fuerte, en el cambio de acorde, sin sobresalto de volumen y sin whoosh — y lo verifica.
- **Verificador del tiempo de lectura:** `scripts/checar-leitura.mjs` lee todo el texto en pantalla y rechaza lo que desaparece antes de que dé
  tiempo a leerlo (1 s + 0,3 s por palabra, mínimo 1,5 s).
- **b-roll automático:** video de una persona hablando + transcripción → plano frase a frase (rostro, trazo del concepto con la
  persona en un círculo, gráfico a pantalla completa) y la plantilla que renderiza ese plano (`scripts/broll-plano.py`, `assets/broll/`).
- **16:9 y 9:16 del mismo proyecto:** el diseño se recalcula según el formato.
- **Prueba antes del render completo** y revisión del MP4 con hojas de fotogramas (`scripts/inspect-video.py`).
- **Tema INEMA listo:** `assets/inema/` (colores, fuentes locales, subtítulos con contorno).

## El proceso, de principio a fin

Quién lo hace: 🧠 sesión contigo · ⚙️ script · 🤖 agente (Claude Code siguiendo el `SKILL.md`). En los comandos, `P` es la carpeta del video (p. ej., `~/videos/trabalho/2026-11-06-meuapp`) y `scripts/` es la del kit (ejecuta desde `~/projetos/video-codigo` o usa la ruta completa).

| # | Paso | Comando / acción | Quién |
|---|---|---|---|
| 1 | Pedir el video | "/video-codigo faz um vídeo de 40 s do meu produto, lê a pasta X" | 🧠 |
| 2 | Responder las 3 preguntas | tema y público · con voz o solo música · estilo (estándar INEMA o referencia) | 🧠 |
| 3 | Leer la fuente y proponer una dirección | brief, guion de planos, duración y formatos | 🤖 |
| 4 | Aprobar la propuesta (si quieres aprobarla) | el agente muestra la propuesta; una orden explícita de producir ya es suficiente | 🧠 |
| 5 | Guion → voz con tiempo por palabra, verificada por Whisper | `python3 scripts/voz.py --projeto P P/roteiro.json [--tentativas 3]` → `voz.wav`, `tiempos.js`, `checagem.md` | ⚙️ |
| 6 | Leer la verificación de voz | abrir `P/voz/<id>/checagem.md` (frases ⚠ y lo que oyó Whisper); rehacer con `--refazer --frase <id>` | 🤖 |
| 7 | Escribir las escenas | partir de `exemplos/explicativo-narrado/` (voz) o `exemplos/lancamento/` (solo música) y cambiar las escenas | 🤖 |
| 8 | Tiempo de lectura + cortes | `node scripts/checar-leitura.mjs --project P --salvar-cortes P/audio/<id>/cortes.json` (y `--width 1080 --height 1920`) → debe dar 0 | ⚙️ + 🤖 |
| 9 | Música ajustada a los cortes y mezcla | `python3 scripts/mezcla.py --projeto P --id <id> --musica tranquila --lufs -14` → `mezcla.wav` + `trilha.json` (da 1 si algo falla) | ⚙️ |
| 10 | Prueba: fotogramas sueltos y un fragmento | `node scripts/render-video.mjs --project P --output prova.png --still 3` (y `--start/--end`) | ⚙️ + 🤖 |
| 11 | Render 16:9 y 9:16 | `node scripts/render-video.mjs --project P --output P/renders/x.mp4 --audio P/audio/<id>/mezcla.wav` (+ `--width 1080 --height 1920`) | ⚙️ |
| 12 | Revisión | `python3 scripts/inspect-video.py P/renders/x.mp4 --output-dir P/reviews` y revisar las hojas | ⚙️ + 🤖 |
| 13 | Entregar | MP4 + portada + proyecto editable; publicar solo con tu OK | 🧠 |

## Modo b-roll (video de una persona hablando)

Para una clase, testimonio o avatar hablando: la grabación no se corta; el kit decide, frase a frase, qué aparece en pantalla.

| Tratamiento | Cuándo | En pantalla |
|---|---|---|
| `rosto` | apertura, opinión, historia, llamada, cierre | la persona completa (o media pantalla con `--rosto-tamanho meia`) |
| `pip` | la frase tiene un concepto | la persona en un círculo en la esquina + el concepto dibujado con trazos (icono + palabra) |
| `cheio` | número, comparación, pasos | gráfico a pantalla completa; el número aparece justo al pronunciarse LA palabra |

Reglas verificadas por el generador: abre y cierra con el rostro, rostro ≤ 8 s seguidos, pantalla completa de 3 a 8 s, nunca dos planos a pantalla completa
seguidos, trazo corto (< 1,8 s) vuelve al rostro, y todo texto permanece el tiempo necesario para leerlo (lo visual se mantiene sobre la frase
siguiente cuando hace falta).

```bash
K=~/projetos/video-codigo; P=~/videos/trabalho/2026-11-07-aula
# 1. transcrição com tempo por palavra (local)
cd ~/projetos/inemavox && venv/bin/python transcrever_v1.py --in aula.mp4 --outdir $P/transcricao --src pt --words
# 2. plano + molde + quadros + áudio  (--rosto = centro x, centro y e raio do rosto; x e y em fração da largura/altura, raio em fração da altura)
python3 $K/scripts/broll-plano.py --fala aula.mp4 --transcricao $P/transcricao/transcript.json --projeto $P --rosto 0.58,0.45,0.38
# 3. revisar $P/plano.md; editar $P/plano.json (tratamento, visual.titulo, visual.icone, itens) e refazer o plano.js
python3 $K/scripts/broll-plano.py --projeto $P --replanejar
# 4. quadros de prova (confira o rosto no círculo) e tempo de leitura
node $K/scripts/render-video.mjs --project $P --output $P/prova.png --still 6
node $K/scripts/checar-leitura.mjs --project $P
# 5. render com o som original
node $K/scripts/render-video.mjs --project $P --output $P/renders/aula-broll.mp4 --audio $P/audio/fala.wav
```

**Para el agente que hará el video:** el plano es un borrador heurístico (sin IA de pago). Lee `plano.md` completo,
cambia lo que no sirve (un número que Whisper oyó mal nunca debe aparecer en pantalla), elige mejores iconos
(`assets/broll/broll.mjs › ICONES`; icono nuevo = rutas SVG en viewBox 100×100) o escribe un visual nuevo en
`VISUAIS` (función `(caixa, v, G) → (t) => pinta`). El video se convierte en fotogramas JPG en `P/quadros/` (Chromium del render no
reproduce H.264 y necesita el fotograma exacto); no incluyas esta carpeta en el control de versiones. Formatos de transcripción aceptados: `transcript.json` y
`words.json` de inemavox, `tempos.json` de `voz.py` o de r7ex, `.srt` (sin tiempo por palabra: peor sincronía).
Regla INEMA para avatares: como máximo media pantalla — para el avatar de Nei usa `--rosto-tamanho meia`.

## Instalación

```bash
git clone https://github.com/inematds/video-codigo ~/projetos/video-codigo
bash ~/projetos/video-codigo/instalar.sh     # conecta la skill con Claude Code/Codex e instala Playwright (sin sudo)
```

Requisitos previos: Node 18+, Python 3 con `numpy`, `scipy` y Pillow, FFmpeg. (Ubuntu/Debian: `sudo apt install python3-numpy python3-scipy python3-pil`.) `instalar.sh` instala Playwright y Chromium (sin sudo); comprueba el resto y muestra el comando correspondiente. **Voz (opcional):** inemavox en `~/projetos/inemavox`, con el entorno Chatterbox (`~/miniconda3/envs/chatterbox`) y Whisper de su
`venv`; la voz de referencia es un archivo `.wav` de 10–20 s (`"voz": "/caminho/minha-voz.wav"` en el guion). Sin voz, la
skill funciona solo con música.

```bash
# voz local (probado: Python 3.11, chatterbox-tts 0.1.6, GPU NVIDIA, Miniconda; los modelos descargan algunos GB la primera vez)
# conda o inemavox en otro lugar: CHATTERBOX_PYTHON=/caminho/python3  INEMAVOX_DIR=/caminho/inemavox
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
| Película de producto de atende-leads (pantallas reales, cursor, voz atada a cada palabra) | película de producto narrada, 61 s (ES) y 63 s (PT) | `exemplos/filme-produto-es/` · `renders/atende-es-16x9.mp4` · `renders/atende-es-9x16.mp4` · PT: `exemplos/filme-produto/` |
| Este vídeo no tiene cámara | explicativo narrado (voz local), 44 s | `exemplos/explicativo-narrado/` · `renders/explicativo-16x9.mp4` · `renders/explicativo-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=tkT2I6nrMAk) |
| INEMA.CLUB en un plano | lanzamiento solo con música, 21 s | `exemplos/lancamento/` · `renders/lancamento-16x9.mp4` · `renders/lancamento-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=IJ-qZQ1drBc) |

El guion del ejemplo narrado usa la voz `nei`, que solo existe en la máquina del autor: para volver a generar la voz, ejecuta `VC_VOZ=/caminho/sua-voz.wav`. Para rehacer solo el vídeo (el audio ya está en el repositorio): `cd exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output x.mp4 --audio audio/lancamento/mezcla.wav`.

## Estructura

```
SKILL.md              instrucciones de la skill (el agente las sigue)
references/           brief, dirección, movimiento, sonido, voz, render, revisión, prompts de película
scripts/              voz.py (voz local) · mezcla.py · render-video.mjs · render-tramos.sh · inspect-video.py · …
assets/inema/         tema INEMA + fuentes locales
assets/voz-sync/      motor de tiempos (imagen sincronizada con la palabra)
exemplos/ renders/    dos vídeos completos y los MP4
guia/                 página de guía (PT/EN/ES)
```

---
[INEMA.CLUB](https://inema.club)
# 🎬 video-codigo — videos made with code

[![Video made with code](guia/assets/banner-en.jpg)](https://inematds.github.io/video-codigo/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

video-codigo is a skill for Claude Code (and Codex) that makes videos without a camera or editing software: each frame is written in code (HTML, Canvas, or SVG) and turned into an MP4. It’s for anyone who wants to present a product, project, or idea in a video—a launch, ad, explainer, product series, or lesson. For narrated videos, the voice is generated on your computer (with no voice-generation fees), and each image appears at the moment its corresponding word is spoken. Requires Node, Python, FFmpeg, and, for voice, inemavox with an NVIDIA GPU (without one, the video has music only).

## 📖 User guide

Complete guide (landing page + walkthrough + examples): **https://inematds.github.io/video-codigo/guia/en/**

## What it does

- **Three questions before starting:** what it’s about and who it’s for; voice or music only; which style.
- **Reads the source:** document, folder, repository, or website — “read everything and propose a video.”
- **Synchronized local voice:** `scripts/voz.py` generates the narration with a cloned voice (Chatterbox) and measures the timing of each
  word (Whisper); the `assets/voz-sync/` engine ties each image to a word (`pal('frase', 'palavra')`).
- **Voice checked by Whisper:** each sentence is listened to again and redone if it doesn’t match (similarity or incorrect number);
  everything goes in `voz/<id>/checagem.md`, including what Whisper heard. `scripts/checar-fala.py` checks it afterward.
- **Original music synthesized and synced to the cuts:** `scripts/mezcla.py` (120 or 84 BPM), very low under the voice;
  each scene cut lands on a strong beat, at the chord change, with no volume jump and no whoosh — and it checks this.
- **Reading-time checker:** `scripts/checar-leitura.mjs` reads all on-screen text and fails anything that disappears before there’s
  time to read it (1 s + 0,3 s per word, minimum 1,5 s).
- **Automatic b-roll:** video of a person speaking + transcript → a sentence-by-sentence plan (face, concept sketch with the
  person in a circle, full-screen graphic) and the template that renders that plan (`scripts/broll-plano.py`, `assets/broll/`).
- **16:9 and 9:16 from the same project:** the layout recalculates for each format.
- **Proof before the full render** and MP4 review with frame sheets (`scripts/inspect-video.py`).
- **INEMA theme ready to use:** `assets/inema/` (colors, local fonts, outlined captions).

## The Process, from Start to Finish

Who does what: 🧠 session with you · ⚙️ script · 🤖 agent (Claude Code following the `SKILL.md`). In the commands, `P` is the video folder (e.g., `~/videos/trabalho/2026-11-06-meuapp`) and `scripts/` is the kit folder (run from inside `~/projetos/video-codigo` or use the full path).

| # | Step | Command / action | Who |
|---|---|---|---|
| 1 | Request the video | "/video-codigo faz um vídeo de 40 s do meu produto, lê a pasta X" | 🧠 |
| 2 | Answer the 3 questions | topic and audience · voice or music only · style (INEMA default or reference) | 🧠 |
| 3 | Read the source and propose a direction | brief, shot list, duration, and formats | 🤖 |
| 4 | Approve the proposal (if you want to approve it) | the agent shows the proposal; an explicit instruction to produce it right away is also enough | 🧠 |
| 5 | Script → voice with word-level timing, checked by Whisper | `python3 scripts/voz.py --projeto P P/roteiro.json [--tentativas 3]` → `voz.wav`, `tiempos.js`, `checagem.md` | ⚙️ |
| 6 | Read the voice check | open `P/voz/<id>/checagem.md` (sentences ⚠ and what Whisper heard); redo with `--refazer --frase <id>` | 🤖 |
| 7 | Write the scenes | start from `exemplos/explicativo-narrado/` (voice) or `exemplos/lancamento/` (music only) and replace the scenes | 🤖 |
| 8 | Reading time + cuts | `node scripts/checar-leitura.mjs --project P --salvar-cortes P/audio/<id>/cortes.json` (and `--width 1080 --height 1920`) → must return 0 | ⚙️ + 🤖 |
| 9 | Music synced to the cuts and mixing | `python3 scripts/mezcla.py --projeto P --id <id> --musica tranquila --lufs -14` → `mezcla.wav` + `trilha.json` (returns 1 if anything fails) | ⚙️ |
| 10 | Proof: still frames and a clip | `node scripts/render-video.mjs --project P --output prova.png --still 3` (and `--start/--end`) | ⚙️ + 🤖 |
| 11 | Render 16:9 and 9:16 | `node scripts/render-video.mjs --project P --output P/renders/x.mp4 --audio P/audio/<id>/mezcla.wav` (+ `--width 1080 --height 1920`) | ⚙️ |
| 12 | Review | `python3 scripts/inspect-video.py P/renders/x.mp4 --output-dir P/reviews` and inspect the sheets | ⚙️ + 🤖 |
| 13 | Deliver | MP4 + cover + editable project; publish only with your OK | 🧠 |

## B-Roll Mode (Video of a Person Speaking)

For a lesson, testimonial, or talking avatar: the recording isn’t cut; the kit decides, sentence by sentence, what appears on screen.

| Treatment | When | On screen |
|---|---|---|
| `rosto` | opening, opinion, story, call to action, closing | the full person (or half screen with `--rosto-tamanho meia`) |
| `pip` | the sentence has a concept | the person in a corner circle + the concept drawn as a line illustration (icon + word) |
| `cheio` | number, comparison, steps | full-screen graphic; the number appears ON the spoken word |

Rules checked by the generator: opens and closes on the face, face ≤ 8 s in a row, full-screen 3 to 8 s, never two full-screen segments
back to back, short illustration (< 1,8 s) returns to the face, and all text stays on screen long enough to be read (the visual holds over the next sentence
when needed).

```bash
K=~/projetos/video-codigo; P=~/videos/trabalho/2026-11-07-aula
# 1. transcription with word-level timing (local)
cd ~/projetos/inemavox && venv/bin/python transcrever_v1.py --in aula.mp4 --outdir $P/transcricao --src pt --words
# 2. plan + template + frames + audio  (--rosto = face center x, center y, and radius; x and y as fractions of width/height, radius as a fraction of height)
python3 $K/scripts/broll-plano.py --fala aula.mp4 --transcricao $P/transcricao/transcript.json --projeto $P --rosto 0.58,0.45,0.38
# 3. review $P/plano.md; edit $P/plano.json (tratamento, visual.titulo, visual.icone, itens) and regenerate plano.js
python3 $K/scripts/broll-plano.py --projeto $P --replanejar
# 4. proof frames (check the face in the circle) and reading time
node $K/scripts/render-video.mjs --project $P --output $P/prova.png --still 6
node $K/scripts/checar-leitura.mjs --project $P
# 5. render with the original sound
node $K/scripts/render-video.mjs --project $P --output $P/renders/aula-broll.mp4 --audio $P/audio/fala.wav
```

**For the agent making the film:** the plan is a heuristic draft (no paid AI). Read all of `plano.md`,
replace anything that doesn’t work (a number Whisper heard incorrectly must never appear on screen), choose better icons
(`assets/broll/broll.mjs › ICONES`; a new icon = SVG paths in viewBox 100×100) or write a new visual in
`VISUAIS` (function `(caixa, v, G) → (t) => pinta`). The video becomes JPG frames in `P/quadros/` (the render’s Chromium doesn’t
play H.264 and needs an exact frame); don’t version this folder. Accepted transcript formats: `transcript.json` and
`words.json` from inemavox, `tempos.json` from `voz.py` or r7ex, `.srt` (no word-level timing: worse sync).
INEMA avatar rule: at most half screen — for Nei’s avatar, use `--rosto-tamanho meia`.

## Installation

```bash
git clone https://github.com/inematds/video-codigo ~/projetos/video-codigo
bash ~/projetos/video-codigo/instalar.sh     # connects the skill to Claude Code/Codex and installs Playwright (without sudo)
```

Prerequisites: Node 18+, Python 3 with `numpy`, `scipy`, and Pillow, and FFmpeg. (Ubuntu/Debian: `sudo apt install python3-numpy python3-scipy python3-pil`.) `instalar.sh` installs Playwright and Chromium (without sudo); it checks for the rest and shows the command to install it. **Voice (optional):** [inemavox](https://github.com/inematds/inemavox) in `~/projetos/inemavox`, with the Chatterbox environment (`~/miniconda3/envs/chatterbox`) and its Whisper `venv`; the reference voice is a 10–20-second `.wav` file (`"voz": "/caminho/minha-voz.wav"` in the script). Without voice, the skill works with music only.

```bash
# local voice (tested: Python 3.11, chatterbox-tts 0.1.6, NVIDIA GPU, Miniconda; models download several GB on first use)
# conda or inemavox elsewhere: CHATTERBOX_PYTHON=/caminho/python3  INEMAVOX_DIR=/caminho/inemavox
git clone https://github.com/inematds/inemavox ~/projetos/inemavox
conda create -n chatterbox python=3.11 -y
~/miniconda3/envs/chatterbox/bin/pip install chatterbox-tts==0.1.6
cd ~/projetos/inemavox && python3 -m venv venv && venv/bin/pip install faster-whisper soundfile numpy
```

Quick installation test (no voice, ~1 min):
`cd ~/projetos/video-codigo/exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output teste.mp4 --audio audio/lancamento/mezcla.wav --overwrite`

## Examples (made with the kit itself)

| Example | Type | Files |
|---|---|---|
| atende-leads product film (real screens, cursor, voice tied to words) | narrated product film, 63 s; Spanish version 61 s | `exemplos/filme-produto/` · `renders/atende-16x9.mp4` · `renders/atende-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=tWv1mEIK62c) · ES: `exemplos/filme-produto-es/` |
| This video has no camera | narrated explainer (local voice), 44 s | `exemplos/explicativo-narrado/` · `renders/explicativo-16x9.mp4` · `renders/explicativo-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=tkT2I6nrMAk) |
| INEMA.CLUB in one shot | launch video with music only, 21 s | `exemplos/lancamento/` · `renders/lancamento-16x9.mp4` · `renders/lancamento-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=IJ-qZQ1drBc) |

The narrated example script uses the `nei` voice, which is only available on the author’s machine. To generate the voice again, run it with `VC_VOZ=/caminho/sua-voz.wav`. To recreate only the video (the audio is already in the repository): `cd exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output x.mp4 --audio audio/lancamento/mezcla.wav`.

## Structure

```
SKILL.md              skill instructions (the agent follows these)
references/           brief, direction, motion, sound, voice, rendering, review, film prompts
scripts/              voz.py (local voice) · mezcla.py · render-video.mjs · render-tramos.sh · inspect-video.py · …
assets/inema/         INEMA theme + local fonts
assets/voz-sync/      timing engine (image synced to word)
exemplos/ renders/    two complete videos and the MP4 files
guia/                 guide page (PT/EN/ES)
```

---
[INEMA.CLUB](https://inema.club)
# 🎬 video-codigo — videos made with code

[![Code-made video](guia/assets/banner-en.jpg)](https://inematds.github.io/video-codigo/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

video-codigo is a skill for Claude Code (and Codex) that makes videos without a camera or an editor: each frame is
written in code (HTML, Canvas or SVG) and turned into an MP4. It’s for anyone who wants to present a product, project or
idea in a video—a launch, ad, explainer, product series or lesson. If the video has narration, the voice is generated on
your computer (no paying for voice generation), and each image appears at the moment the word is spoken. You need Node,
Python, FFmpeg and, for voice, inemavox with an NVIDIA GPU (without one, the video is produced with music only).

## 📖 User guide

Complete guide (landing page + walkthrough + examples): **https://inematds.github.io/video-codigo/guia/en/**

## What it does

- **Three questions before getting started:** what it’s about and who it’s for; voice or music only; and style.
- **Reads the source:** a document, folder, repository or website—“read everything and suggest a video.”
- **Synchronized local voice:** `scripts/voz.py` generates narration with a cloned voice (Chatterbox) and measures the timing of each
  word (Whisper); the `assets/voz-sync/` engine pins each image to a word (`pal('frase', 'palavra')`).
- **Synthesized original music:** `scripts/mezcla.py` (120 or 84 BPM), mixed very quietly under the voice.
- **16:9 and 9:16 from the same project:** the layout recalculates for each format.
- **Preview before the full render** and MP4 review with frame sheets (`scripts/inspect-video.py`).
- **INEMA theme ready to use:** `assets/inema/` (colors, local fonts, outlined captions).

## The process, from start to finish

Who does what: 🧠 session with you · ⚙️ script · 🤖 agent (Claude Code following `SKILL.md`). In the commands, `P` is the video folder (e.g. `~/videos/trabalho/2026-11-06-meuapp`) and `scripts/` is the kit’s folder (run commands from `~/projetos/video-codigo` or use the full path).

| # | Step | Command / action | Who |
|---|---|---|---|
| 1 | Request the video | "/video-codigo make a 40-second video of my product; read folder X" | 🧠 |
| 2 | Answer the 3 questions | topic and audience · voice or music only · style (INEMA default or reference) | 🧠 |
| 3 | Read the source and suggest a direction | brief, shot outline, duration and formats | 🤖 |
| 4 | Approve the proposal (if you want to) | the agent shows the proposal; an explicit instruction to produce is enough to proceed | 🧠 |
| 5 | Script → voice with word-level timing | `python3 scripts/voz.py --projeto P P/roteiro.json` → `voz.wav`, `tiempos.js` | ⚙️ |
| 6 | Music and mixing | `python3 scripts/mezcla.py --projeto P --id <id> --musica tranquila --lufs -14` | ⚙️ |
| 7 | Write the scenes | start from `exemplos/explicativo-narrado/` (voice) or `exemplos/lancamento/` (music only) and replace the scenes | 🤖 |
| 8 | Preview: still frames and a clip | `node scripts/render-video.mjs --project P --output prova.png --still 3` (and `--start/--end`) | ⚙️ + 🤖 |
| 9 | Render in 16:9 and 9:16 | `node scripts/render-video.mjs --project P --output P/renders/x.mp4 --audio P/audio/<id>/mezcla.wav` (+ `--width 1080 --height 1920`) | ⚙️ |
| 10 | Review | `python3 scripts/inspect-video.py P/renders/x.mp4 --output-dir P/reviews` and inspect the frame sheets | ⚙️ + 🤖 |
| 11 | Deliver | MP4 + cover + editable project; publish only with your OK | 🧠 |

## Installation

```bash
git clone https://github.com/inematds/video-codigo ~/projetos/video-codigo
bash ~/projetos/video-codigo/instalar.sh     # connects the skill to Claude Code/Codex and installs Playwright (no sudo)
```

Prerequisites: Node 18+, Python 3 with `numpy` and Pillow, FFmpeg. **Voice (optional):** inemavox at
[https://github.com/inematds/inemavox](https://github.com/inematds/inemavox) in `~/projetos/inemavox`, with the Chatterbox environment (`~/miniconda3/envs/chatterbox`) and its Whisper `venv`; the reference voice is a 10–20 s `.wav` file (`"voz": "/caminho/minha-voz.wav"` in the script). Without voice, the
skill works with music only.

## Examples (made with the kit itself)

| Example | Type | Files |
|---|---|---|
| This video has no camera | narrated explainer (local voice), 44 s | `exemplos/explicativo-narrado/` · `renders/explicativo-16x9.mp4` · `renders/explicativo-9x16.mp4` |
| INEMA.CLUB in one shot | launch video with music only, 21 s | `exemplos/lancamento/` · `renders/lancamento-16x9.mp4` · `renders/lancamento-9x16.mp4` |

To rerender an example: `cd exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output x.mp4 --audio audio/lancamento/mezcla.wav`.

## Structure

```
SKILL.md              skill instructions (the agent follows these)
references/           brief, direction, motion, sound, voice, render, review, film prompts
scripts/              voz.py (local voice) · mezcla.py · render-video.mjs · render-tramos.sh · inspect-video.py · …
assets/inema/         INEMA theme + local fonts
assets/voz-sync/      timing engine (image pinned to word)
exemplos/ renders/    two complete videos and their MP4s
guia/                 guide page (PT/EN/ES)
```

---
[INEMA.CLUB](https://inema.club)
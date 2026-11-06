# 🎬 video-codigo — vídeos feitos com código

[![Vídeo com código](guia/assets/banner.jpg)](https://inematds.github.io/video-codigo/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O video-codigo é uma skill para o Claude Code (e o Codex) que faz vídeos sem câmera e sem editor: cada quadro é
escrito em código (HTML, Canvas ou SVG) e vira MP4. Serve para quem quer mostrar um produto, um projeto ou uma ideia em
vídeo — lançamento, anúncio, explicativo, série de produtos ou aula. Se o vídeo for narrado, a voz é gerada no seu
computador (sem pagar por voz) e cada imagem entra no instante em que a palavra é dita. Precisa de Node, Python, FFmpeg e,
para a voz, do inemavox com GPU NVIDIA (sem ela, o vídeo sai só com música).

## 📖 Guia de uso

Guia completo (landing + passo a passo + exemplos): **https://inematds.github.io/video-codigo/guia/**

## O que ele faz

- **Três perguntas antes de começar:** sobre o que é e para quem; com voz ou só com música; qual estilo.
- **Lê a fonte:** documento, pasta, repositório ou site — "lê tudo e me propõe um vídeo".
- **Voz local sincronizada:** `scripts/voz.py` gera a narração com a voz clonada (Chatterbox) e mede o tempo de cada
  palavra (Whisper); o motor `assets/voz-sync/` prende cada imagem a uma palavra (`pal('frase', 'palavra')`).
- **Música original sintetizada:** `scripts/mezcla.py` (120 ou 84 BPM), bem baixa debaixo da voz.
- **16:9 e 9:16 do mesmo projeto:** o layout se recalcula por formato.
- **Prova antes do render inteiro** e revisão do MP4 com folhas de quadros (`scripts/inspect-video.py`).
- **Tema INEMA pronto:** `assets/inema/` (cores, fontes locais, legenda com contorno).

## O processo, do início ao fim

Quem faz: 🧠 sessão com você · ⚙️ script · 🤖 agente (Claude Code seguindo o `SKILL.md`). Nos comandos, `P` é a pasta do vídeo (ex.: `~/videos/trabalho/2026-11-06-meuapp`) e `scripts/` é a do kit (rode de dentro de `~/projetos/video-codigo` ou use o caminho completo).

| # | Passo | Comando / ação | Quem |
|---|---|---|---|
| 1 | Pedir o vídeo | "/video-codigo faz um vídeo de 40 s do meu produto, lê a pasta X" | 🧠 |
| 2 | Responder as 3 perguntas | assunto e público · com voz ou só música · estilo (padrão INEMA ou referência) | 🧠 |
| 3 | Ler a fonte e propor direção | brief, roteiro de planos, duração e formatos | 🤖 |
| 4 | Aprovar a proposta (se você quiser aprovar) | o agente mostra a proposta; ordem explícita de produzir já vale | 🧠 |
| 5 | Roteiro → voz com tempo por palavra | `python3 scripts/voz.py --projeto P P/roteiro.json` → `voz.wav`, `tiempos.js` | ⚙️ |
| 6 | Música e mixagem | `python3 scripts/mezcla.py --projeto P --id <id> --musica tranquila --lufs -14` | ⚙️ |
| 7 | Escrever as cenas | partir de `exemplos/explicativo-narrado/` (voz) ou `exemplos/lancamento/` (só música) e trocar as cenas | 🤖 |
| 8 | Prova: quadros soltos e um trecho | `node scripts/render-video.mjs --project P --output prova.png --still 3` (e `--start/--end`) | ⚙️ + 🤖 |
| 9 | Render 16:9 e 9:16 | `node scripts/render-video.mjs --project P --output P/renders/x.mp4 --audio P/audio/<id>/mezcla.wav` (+ `--width 1080 --height 1920`) | ⚙️ |
| 10 | Revisão | `python3 scripts/inspect-video.py P/renders/x.mp4 --output-dir P/reviews` e olhar as folhas | ⚙️ + 🤖 |
| 11 | Entregar | MP4 + capa + projeto editável; publicar só com o seu OK | 🧠 |

## Instalação

```bash
git clone https://github.com/inematds/video-codigo ~/projetos/video-codigo
bash ~/projetos/video-codigo/instalar.sh     # liga a skill no Claude Code/Codex e instala o Playwright (sem sudo)
```

Pré-requisitos: Node 18+, Python 3 com `numpy` e Pillow, FFmpeg. **Voz (opcional):** o
[inemavox](https://github.com/inematds/inemavox) em `~/projetos/inemavox` com o ambiente Chatterbox (`~/miniconda3/envs/chatterbox`) e o Whisper do
`venv` dele; a voz de referência é um `.wav` de 10–20 s (`"voz": "/caminho/minha-voz.wav"` no roteiro). Sem voz, a
skill funciona só com música.

```bash
# voz local (testado: Python 3.11, chatterbox-tts 0.1.6, GPU NVIDIA)
git clone https://github.com/inematds/inemavox ~/projetos/inemavox
conda create -n chatterbox python=3.11 -y
~/miniconda3/envs/chatterbox/bin/pip install chatterbox-tts==0.1.6
cd ~/projetos/inemavox && python3 -m venv venv && venv/bin/pip install faster-whisper soundfile numpy
```

Teste rápido da instalação (sem voz, ~1 min):
`cd ~/projetos/video-codigo/exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output teste.mp4 --audio audio/lancamento/mezcla.wav`

## Exemplos (feitos com o próprio kit)

| Exemplo | Tipo | Arquivos |
|---|---|---|
| Este vídeo não tem câmera | explicativo narrado (voz local), 44 s | `exemplos/explicativo-narrado/` · `renders/explicativo-16x9.mp4` · `renders/explicativo-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=tkT2I6nrMAk) |
| INEMA.CLUB em um plano | lançamento só com música, 21 s | `exemplos/lancamento/` · `renders/lancamento-16x9.mp4` · `renders/lancamento-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=IJ-qZQ1drBc) |

Para refazer um exemplo: `cd exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output x.mp4 --audio audio/lancamento/mezcla.wav`.

## Estrutura

```
SKILL.md              instruções da skill (o agente segue isto)
references/           brief, direção, movimento, som, voz, render, revisão, prompts de filme
scripts/              voz.py (voz local) · mezcla.py · render-video.mjs · render-tramos.sh · inspect-video.py · …
assets/inema/         tema INEMA + fontes locais
assets/voz-sync/      motor de tempo (imagem presa à palavra)
exemplos/ renders/    dois vídeos completos e os MP4
guia/                 página de guia (PT/EN/ES)
```

---
[INEMA.CLUB](https://inema.club)

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
- **Voz conferida pelo Whisper:** cada frase é ouvida de novo e refeita se não bate (semelhança ou número errado);
  tudo fica em `voz/<id>/checagem.md`, com o que o Whisper ouviu. `scripts/checar-fala.py` confere depois.
- **Música original sintetizada e presa aos cortes:** `scripts/mezcla.py` (120 ou 84 BPM), bem baixa debaixo da voz;
  cada corte de cena cai num tempo forte, na troca de acorde, sem susto de volume e sem whoosh — e ele confere isso.
- **Verificador de tempo de leitura:** `scripts/checar-leitura.mjs` lê todo texto da tela e reprova o que some antes de dar
  tempo de ler (1 s + 0,3 s por palavra, mínimo 1,5 s).
- **b-roll automático:** vídeo de pessoa falando + transcrição → plano frase a frase (rosto, traço do conceito com a
  pessoa num círculo, gráfico em tela cheia) e o molde que renderiza esse plano (`scripts/broll-plano.py`, `assets/broll/`).
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
| 5 | Roteiro → voz com tempo por palavra, conferida pelo Whisper | `python3 scripts/voz.py --projeto P P/roteiro.json [--tentativas 3]` → `voz.wav`, `tiempos.js`, `checagem.md` | ⚙️ |
| 6 | Ler a checagem da voz | abrir `P/voz/<id>/checagem.md` (frases ⚠ e o que o Whisper ouviu); refazer com `--refazer --frase <id>` | 🤖 |
| 7 | Escrever as cenas | partir de `exemplos/explicativo-narrado/` (voz) ou `exemplos/lancamento/` (só música) e trocar as cenas | 🤖 |
| 8 | Tempo de leitura + cortes | `node scripts/checar-leitura.mjs --project P --salvar-cortes P/audio/<id>/cortes.json` (e `--width 1080 --height 1920`) → tem de sair 0 | ⚙️ + 🤖 |
| 9 | Música presa aos cortes e mixagem | `python3 scripts/mezcla.py --projeto P --id <id> --musica tranquila --lufs -14` → `mezcla.wav` + `trilha.json` (sai 1 se algo falhar) | ⚙️ |
| 10 | Prova: quadros soltos e um trecho | `node scripts/render-video.mjs --project P --output prova.png --still 3` (e `--start/--end`) | ⚙️ + 🤖 |
| 11 | Render 16:9 e 9:16 | `node scripts/render-video.mjs --project P --output P/renders/x.mp4 --audio P/audio/<id>/mezcla.wav` (+ `--width 1080 --height 1920`) | ⚙️ |
| 12 | Revisão | `python3 scripts/inspect-video.py P/renders/x.mp4 --output-dir P/reviews` e olhar as folhas | ⚙️ + 🤖 |
| 13 | Entregar | MP4 + capa + projeto editável; publicar só com o seu OK | 🧠 |

## Modo b-roll (vídeo de pessoa falando)

Para aula, depoimento ou avatar falando: a gravação não é cortada; o kit decide, frase a frase, o que a tela mostra.

| Tratamento | Quando | Na tela |
|---|---|---|
| `rosto` | abertura, opinião, história, chamada, fechamento | a pessoa inteira (ou meia tela com `--rosto-tamanho meia`) |
| `pip` | a frase tem um conceito | a pessoa num círculo no canto + o conceito desenhado em traço (ícone + palavra) |
| `cheio` | número, comparação, passos | gráfico em tela cheia; o número cai NA palavra dita |

Regras conferidas pelo gerador: abre e fecha no rosto, rosto ≤ 8 s seguidos, cheio de 3 a 8 s, nunca dois cheios
colados, traço curto (< 1,8 s) volta ao rosto, e todo texto fica o tempo de ser lido (o visual segura sobre a frase
seguinte quando precisa).

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

**Para o agente que vai fazer o filme:** o plano é um rascunho por heurística (sem IA paga). Leia `plano.md` inteiro,
troque o que não serve (um número que o Whisper ouviu errado nunca vai para a tela), escolha ícones melhores
(`assets/broll/broll.mjs › ICONES`; ícone novo = caminhos SVG em viewBox 100×100) ou escreva um visual novo em
`VISUAIS` (função `(caixa, v, G) → (t) => pinta`). O vídeo vira quadros JPG em `P/quadros/` (o Chromium do render não
toca H.264 e precisa de quadro exato); não versione essa pasta. Formatos aceitos de transcrição: `transcript.json` e
`words.json` do inemavox, `tempos.json` do `voz.py` ou do r7ex, `.srt` (sem tempo por palavra: pior sincronia).
Regra INEMA de avatar: no máximo meia tela — para avatar do Nei use `--rosto-tamanho meia`.

## Instalação

```bash
git clone https://github.com/inematds/video-codigo ~/projetos/video-codigo
bash ~/projetos/video-codigo/instalar.sh     # liga a skill no Claude Code/Codex e instala o Playwright (sem sudo)
```

Pré-requisitos: Node 18+, Python 3 com `numpy`, `scipy` e Pillow, FFmpeg. (Ubuntu/Debian: `sudo apt install python3-numpy python3-scipy python3-pil`.) O `instalar.sh` instala o Playwright e o Chromium (sem sudo); o resto ele confere e mostra o comando. **Voz (opcional):** o
[inemavox](https://github.com/inematds/inemavox) em `~/projetos/inemavox` com o ambiente Chatterbox (`~/miniconda3/envs/chatterbox`) e o Whisper do
`venv` dele; a voz de referência é um `.wav` de 10–20 s (`"voz": "/caminho/minha-voz.wav"` no roteiro). Sem voz, a
skill funciona só com música.

```bash
# voz local (testado: Python 3.11, chatterbox-tts 0.1.6, GPU NVIDIA, Miniconda; os modelos baixam alguns GB no 1º uso)
# conda ou inemavox em outro lugar: CHATTERBOX_PYTHON=/caminho/python3  INEMAVOX_DIR=/caminho/inemavox
git clone https://github.com/inematds/inemavox ~/projetos/inemavox
conda create -n chatterbox python=3.11 -y
~/miniconda3/envs/chatterbox/bin/pip install chatterbox-tts==0.1.6
cd ~/projetos/inemavox && python3 -m venv venv && venv/bin/pip install faster-whisper soundfile numpy
```

Teste rápido da instalação (sem voz, ~1 min):
`cd ~/projetos/video-codigo/exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output teste.mp4 --audio audio/lancamento/mezcla.wav --overwrite`

## Exemplos (feitos com o próprio kit)

| Exemplo | Tipo | Arquivos |
|---|---|---|
| Filme de produto do atende-leads (telas reais, cursor, voz presa à palavra) | filme de produto narrado, 63 s; versão ES 61 s | `exemplos/filme-produto/` · `renders/atende-16x9.mp4` · `renders/atende-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=tWv1mEIK62c) · ES: `exemplos/filme-produto-es/` |
| Este vídeo não tem câmera | explicativo narrado (voz local), 44 s | `exemplos/explicativo-narrado/` · `renders/explicativo-16x9.mp4` · `renders/explicativo-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=tkT2I6nrMAk) |
| INEMA.CLUB em um plano | lançamento só com música, 21 s | `exemplos/lancamento/` · `renders/lancamento-16x9.mp4` · `renders/lancamento-9x16.mp4` · [YouTube](https://www.youtube.com/watch?v=IJ-qZQ1drBc) |
| b-roll sobre um avatar falando (33 s): plano gerado + folha de quadros do render | modo b-roll (rosto · traço · passos em tela cheia) | `exemplos/broll-plano/` (`plano.md`, `plano.json`, `folha.jpg`; o vídeo de origem não vai no repositório) |

O roteiro do exemplo narrado usa a voz `nei`, que só existe na máquina do autor: para gerar de novo a voz, rode com `VC_VOZ=/caminho/sua-voz.wav`. Para refazer só o vídeo (o áudio já está no repositório): `cd exemplos/lancamento && node ../../scripts/render-video.mjs --project . --output x.mp4 --audio audio/lancamento/mezcla.wav`.

## Estrutura

```
SKILL.md              instruções da skill (o agente segue isto)
references/           brief, direção, movimento, som, voz, render, revisão, prompts de filme
scripts/              voz.py (voz local) · checar-fala.py · mezcla.py · checar-leitura.mjs · broll-plano.py · render-video.mjs · …
assets/broll/         molde do b-roll (pessoa falando + traço + gráfico)
assets/inema/         tema INEMA + fontes locais
assets/voz-sync/      motor de tempo (imagem presa à palavra)
exemplos/ renders/    dois vídeos completos e os MP4
guia/                 página de guia (PT/EN/ES)
```

---
[INEMA.CLUB](https://inema.club)

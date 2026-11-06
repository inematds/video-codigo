# Voz, som e sincronia

Leia quando o vídeo tiver voz, ou quando tiver só música e efeitos sintetizados.

## 0 · A primeira pergunta: com voz ou só com som?

Não presuma que haverá voz. Antes de tudo:

> «Você quer **com voz** (narrado, com a sua voz clonada no computador) ou **só dinâmico, com música**?»

- **Com voz** → roteiro, voz local, imagem atada a cada palavra, mixagem com a música bem baixa.
- **Só com som** → a música marca o relógio (`beat-grid.py` ou a música sintetizada do `mezcla.py`). Sem `voz.py`.

## 1 · Roteiro → `roteiro.json`

```json
{"id": "venda", "pausa": 0.2, "intervalo_blocos": 0.6, "voz": "nei",
 "dicionario": [["16:9", "dezesseis por nove"]],
 "blocos": [{"id": "abertura", "frases": [{"id": "hook", "texto": "…"}, {"id": "zero", "texto": "Zero teoria."}]}]}
```

- Uma frase = um instante ao qual a imagem se prende. `id` curtos e com sentido (`hook`, `dia1`, `preco`), sem repetir.
- `pausa`: 0,2 s em venda (rápido), ~0,3 s em explicativo (respira). `intervalo_blocos`: ~0,6–1 s entre capítulos.
- As chaves em espanhol do formato antigo (`bloques`, `hueco_bloques`, `diccionario`) também são aceitas.

## 2 · Voz → `scripts/voz.py` (local, sem API, sem custo)

```bash
python3 scripts/voz.py --projeto P P/roteiro.json --simular          # mostra o que seria gerado
python3 scripts/voz.py --projeto P P/roteiro.json                    # gera (cache por frase)
python3 scripts/voz.py --projeto P P/roteiro.json --refazer --frase hook   # refaz só uma frase
```

Como funciona:
1. Cada frase é falada pelo **Chatterbox** (inemavox, GPU) com a voz clonada de `voz` no roteiro ou `VC_VOZ`
   (nome de um `.wav` em `VC_VOZES` ou caminho de um `.wav`; padrão `nei`).
2. O **Whisper large-v3** local ouve cada frase, mede a semelhança com o texto e dá o tempo de cada palavra.
   Frase abaixo de `VC_SIM_MIN` (0,80) é gerada de novo, até 2 vezes. O que continuar baixo aparece com ⚠.
3. Cada frase é cortada da 1ª à última palavra ouvida (some a respiração ou o ruído do fim) e juntada com `pausa`.

- **Pronúncia:** o texto da tela e o que a voz lê são diferentes. `DICIONARIO` (no script) e `dicionario` (no roteiro)
  trocam «Claude» → «Clód», «IA» → «i a», «16:9» → «dezesseis por nove». Ano e número sempre por extenso.
- **⚠ que não é erro:** o Whisper escreve número em algarismo («16x9») e baixa a semelhança mesmo com a fala certa.
  Ouça o trecho antes de refazer.
- **Saída:** `P/voz/<id>/voz.wav`, `tiempos.json` e `tiempos.js` (`window.TIEMPOS`, com `bloques`, `frases` e `palabras`).
- **Sua própria voz:** grave 10–20 s limpos em `.wav` e use `"voz": "/caminho/minha-voz.wav"`.

## 3 · Imagem atada à voz → `assets/voz-sync/`

Copie `engine.mjs`, `declarativo.mjs` e `motion.mjs` para o projeto. Carregue `tiempos.js` antes do módulo.

- `ini('frase')`, `fin('frase')`, `pal('frase', 'palavra', n)`: o instante exato em que algo é dito.
- `Film`: cenas com `[início, fim)` e `render(t)`. `arrancar(film)` cria `videoSpec`, `seek` e `renderReady`.
- `pop`, `win`, `ease`, `sp`, `count`, `type`, `tap`, `fill`: entradas, presença, molas, contadores, digitação, toques e barras — tudo função de `t`.
- `chat(view, col)`: conversa que desce sozinha (mensagens com `data-t`); `subtitulos(box, {max})`: legenda palavra a palavra (INEMA: `max: 3`).
- **Declarativo** (`preparar(raiz)`), para peças longas: cada elemento diz no HTML quando entra.
  `data-in="frase@palavra"` = quando a voz diz essa palavra; `data-out`, `data-a="up|left|right|scale|fade"`,
  `data-on` (põe a classe `on`). Aceita `+.3`, `-.2`, `:fin` e `#2` (segunda aparição).
- Se uma palavra do roteiro mudar e um `pal()` ou `data-in` não a achar, o render para dizendo qual.

Regras que vieram das revisões:
- **Quadro 0 com conteúdo** (título e protagonista já na tela): é a miniatura antes do play.
- Rótulos **dentro do quadro** (confira a borda direita) e nunca em cima da legenda.
- Caso inventado sempre com rótulo visível («Caso de exemplo»).

## 4 · Som → `scripts/mezcla.py`

```bash
python3 scripts/mezcla.py --proyecto P --id venda --musica tranquila --lufs -14            # com voz
python3 scripts/mezcla.py --proyecto P --id teaser --duracion 30 --musica energica --lufs -14   # só música
```

- Música original sintetizada (`energica` 120 BPM, `tranquila` 84 BPM) ou `--pista` própria com licença.
- **Com voz, a música vai bem baixo:** 24 dB abaixo da voz quando se fala (`--bajo-voz`), sobe 10 dB nas pausas (`--agache`).
- Efeitos em `P/audio/<id>/eventos.json`, nos mesmos instantes da imagem (`"t": "frase@palavra"`). No padrão INEMA,
  reel e short ficam **sem efeito no meio** (só voz + trilha); use efeito só para marcar uma ação que pede som.
- Sonoridade final: −14 LUFS; pico real ≤ −1,5 dB.

## 5 · Render → `scripts/render-tramos.sh`

```bash
bash scripts/render-tramos.sh P venda/index.html P/renders/venda.mp4 91.633 P/audio/venda/mezcla.wav
```

Em trechos de 60 s: não precisa de ~1,7 GB livres para os quadros de um vídeo de 9 min. Se parar, rode de novo e ele
continua de onde estava. Se o Playwright disser que falta o navegador, rode `bash scripts/preparar-entorno.sh`.

## 6 · Entrega

MP4 + capa + roteiro ao lado do MP4; projeto editável com README e `render.sh`. Nada é publicado sem OK.

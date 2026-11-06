# Som e ritmo

## Música como parte da história

Escolha uma faixa fornecida, um recurso com licença adequada ou uma composição original feita com uma ferramenta disponível. Na síntese por código, planeje estrutura, harmonia, instrumentação e mixagem; um loop de percussão não garante uma direção musical. Não ative pagamentos, clone vozes nem presuma que há créditos sem autorização e condições reais.

Crie abertura, desenvolvimento, contraste e encerramento. Não corte frases musicais ao atingir a duração desejada. Separe voz, música e efeitos quando houver stems. Associe efeitos a ações importantes; evite um whoosh em cada objeto. Deixe espaço para a leitura e a voz local (scripts/voz.py: Chatterbox + Whisper no computador, sem custo).

## Relógio comum

Para uma composição nova com tempo e origem conhecidos:

```bash
python3 scripts/beat-grid.py --bpm 128 --duration 30 --offset 0 --output beats.json
```

Para uma faixa existente:

```bash
python3 scripts/beat-grid.py --audio audio/track.wav --output beats.json
```

A detecção pelo librosa é uma estimativa. Confira fase, silêncios e mudanças de tempo ouvindo a faixa. O script deixa `downbeats` vazio até receber `--downbeat-index N` em áudio analisado; ele não adivinha o primeiro pulso do compasso. `--meter` indica quantos pulsos há por compasso. Para tempo variável, mantenha as marcações medidas e corrija-as conforme a escuta, sem impor uma grade uniforme.

O JSON registra procedência, BPM, pulsos, compassos e possíveis onsets. Os onsets não são necessariamente batidas de bateria: escolha os que forem úteis. Faça a animação e a síntese usarem as mesmas marcações. Salve eventos com tempo, objeto, ação e efeito. Ao renderizar um trecho, recorte o áudio e o vídeo a partir da mesma origem.

## Sincronia e mixagem

Posicione o momento perceptivo importante sobre o acento escolhido; nem todo movimento precisa começar em uma batida. Varie a energia e deixe pausas úteis. Ouça o início, a resolução, as transições, o equilíbrio e os cliques.

Meça o nível integrado e o pico verdadeiro após a codificação. Como ponto de partida para uma peça para redes sociais, considere cerca de −14 LUFS e pelo menos 1 dB de margem de pico verdadeiro; ajuste conforme o material, a plataforma e o briefing. A medição não substitui a escuta.

```bash
ffmpeg -hide_banner -i final.mp4 -vn -af ebur128=peak=true -f null -
```

Não declare que há sincronia audível com base no BPM informado, nos metadados ou nas imagens. Se não for possível ouvir, deixe a verificação pendente e entregue a peça como prova, indicando essa limitação.
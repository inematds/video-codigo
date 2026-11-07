# FALHAS — video-codigo

Uma linha por falha: data, o que quebrou, menor correção, prompt | infra. Mais recente no topo.

| data | o que quebrou | menor correção | tipo |
|---|---|---|---|
| 07/11/2026 | TTS leu "16:9" como "16 maio a 9" e passou (semelhança 0,80 no limite) | dicionário do voz.py troca formato de tela por "16 por 9"; checagem.md mostra o ouvido | infra |
| 07/11/2026 | Whisper escreve "20" e o roteiro "vinte": semelhança caía sem erro real (e número trocado passava) | _alinhar.py normaliza 0–999 e reprova número diferente | infra |
| 07/11/2026 | música subia 8–10 dB em cada pausa curta da voz → susto no corte de cena | mezcla.py segura a música abaixada em pausas < 1,5 s (`--respiro`) e confere salto no corte | infra |
| 06/11/2026 | voz dos exemplos com tom ruim e siglas mal pronunciadas (VPS, lead) e vídeo ainda fraco frente ao original | ouvir a voz antes de publicar (não confiar só na semelhança do Whisper) e comparar com os vídeos originais em tamanho cheio, áudio incluso; ver pendencias.md | prompt + infra |
| 06/11/2026 | erro de `pal()` (palavra fora do roteiro) aparecia como "Ancho/alto deben ser enteros" | render-video.mjs para e mostra os erros da página antes de validar o `videoSpec` | infra |
| 06/11/2026 | checagem do guia em 390 px rodou contra outro site (porta 8765 já ocupada) | porta livre escolhida pelo sistema (`bind 0`) e conferir o `title` da página | infra |
| 06/11/2026 | `mezcla.py` quebrava com "operands could not be broadcast" (1 amostra a menos) | `n = len(voz)` em vez de `int(dur*SR)` | infra |
| 06/11/2026 | buracos de 2–3 s entre frases na voz (sobra de ruído do Chatterbox) | `voz.py` corta cada frase da 1ª à última palavra ouvida | infra |
| 06/11/2026 | fontes caíam para serifada no render | woff2 copiados eram subconjunto; usar Sora.ttf e Inter TTF completos | infra |
| 06/11/2026 | quadro 0 vazio e balão descentralizado no 1º render de prova | 1ª cena com opacidade 1 em t=0; centralizar com margin auto (o `pop` reescreve `transform`) | prompt |

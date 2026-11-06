# FALHAS — video-codigo

Uma linha por falha: data, o que quebrou, menor correção, prompt | infra. Mais recente no topo.

| data | o que quebrou | menor correção | tipo |
|---|---|---|---|
| 06/11/2026 | erro de `pal()` (palavra fora do roteiro) aparecia como "Ancho/alto deben ser enteros" | render-video.mjs para e mostra os erros da página antes de validar o `videoSpec` | infra |
| 06/11/2026 | checagem do guia em 390 px rodou contra outro site (porta 8765 já ocupada) | porta livre escolhida pelo sistema (`bind 0`) e conferir o `title` da página | infra |
| 06/11/2026 | `mezcla.py` quebrava com "operands could not be broadcast" (1 amostra a menos) | `n = len(voz)` em vez de `int(dur*SR)` | infra |
| 06/11/2026 | buracos de 2–3 s entre frases na voz (sobra de ruído do Chatterbox) | `voz.py` corta cada frase da 1ª à última palavra ouvida | infra |
| 06/11/2026 | fontes caíam para serifada no render | woff2 copiados eram subconjunto; usar Sora.ttf e Inter TTF completos | infra |
| 06/11/2026 | quadro 0 vazio e balão descentralizado no 1º render de prova | 1ª cena com opacidade 1 em t=0; centralizar com margin auto (o `pop` reescreve `transform`) | prompt |

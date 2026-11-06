# Movimento e continuidade

Faça o movimento mudar uma relação: conexões, transformação ou causa e resultado. Planeje a geometria e o ritmo antes dos enfeites. Dê à câmera um objetivo e uma trajetória; não use um zoom global como sinônimo de dinamismo.

| Mecanismo | Uso | Condição |
| --- | --- | --- |
| Objeto persistente | Botão que se expande em painel; dado que se transforma em resultado | Preserve a identidade geométrica |
| Montagem | Partes que formam uma solução | Mostre as dependências |
| Reenquadramento | Do detalhe ao sistema e vice-versa | Termine em um foco legível |
| Máscara e mudança de forma | Cartão que se transforma em gráfico | Coordene geometria e conteúdo |
| Tipografia cinética | Mensagem que se transforma em ação | Alinhe movimento e significado |
| Traçado | Percursos e conexões | Mantenha ordem causal e velocidade perceptível |

Varie as curvas e as velocidades com intenção. Evite quiques em textos que precisam se estabilizar rápido. Dê tempo para o resultado de uma ação rápida aparecer.

## Utilidade opcional

Copie `assets/motion/motion.mjs` para o projeto. Ele exporta `spring`, `track`, `mix`, `clamp`, `morphBox`, `camera` e `noise`. São funções de tempo sem estado acumulado. `spring` resolve amortecimento baixo, crítico e alto; `track` soma respostas a mudanças de objetivo. Use segundos absolutos.

```js
import {track, morphBox} from './motion.mjs';
const states = [
  {t: 0, x: 160, y: 320, w: 180, h: 80, r: 40},
  {t: 1.1, x: 70, y: 240, w: 360, h: 260, r: 24},
  {t: 2.7, x: 130, y: 300, w: 240, h: 100, r: 16}
];
const box = morphBox(t, states, {frequency: 2.4, damping: 1});
const focus = track(t, [[0, 0], [1.2, 1], [2.6, 0]], {damping: 1});
```

A base Canvas transforma uma forma em gráfico e resultado; a base SVG demonstra um mecanismo equivalente. São exemplos de movimento, não estilos padrão. Adapte a composição, os recursos e as curvas ao brief.

## Câmera e texto

Desenhe em coordenadas de cena e aplique a câmera uma única vez. Quando necessário, use uma camada posterior para manter o texto nítido. Recalcule o layout conforme a proporção, sem esticar nem cortar uma composição feita para outro formato.

Ordene as mudanças: inicie a geometria, retire o conteúdo, revele o conteúdo novo e deixe-o se estabilizar. Faça o texto entrar em um intervalo de baixa velocidade. Mantenha as posições contínuas quando mudar o objetivo.

## Desfoque temporal

Os renderizadores aceitam `--subframes 1|2|4|8` e `--shutter 0..1`. Teste uma ação com 1 e 4 amostras. A média temporal aumenta o custo aproximadamente conforme o número de amostras e pode borrar o texto. Use-a apenas se melhorar o movimento observado.
# Modelo · Filme de lançamento por blocos

Esta é a estrutura que mais gerou “uau”. Ela veio de um prompt de filme de lançamento que circulava no X em outubro de 2026. Reescrevemos e ampliamos com o que aprendemos ao produzir dois filmes reais com ela.

**Como usar:**
1. Preencha tudo o que estiver entre `[colchetes]`. Se não souber algo, deixe em branco e peça ao Claude: «Preencha este modelo com o que você sabe sobre [produto] e me pergunte o que estiver faltando».
2. Cole o resultado em uma conversa nova com a skill instalada.
3. Claude pedirá os materiais e mostrará o mapa de pulsos e alguns quadros **antes** de escrever o filme. É nessa hora que você pode corrigir o rumo.

Há dois exemplos completos preenchidos em `03-exemplo-lancamento.md` e `04-exemplo-explicativo.md`.

---

## Para que serve cada bloco

| Bloco | Para que serve | Se você o remover… |
| --- | --- | --- |
| `<inputs>` | Lista o que Claude precisa pedir antes de começar | Ele inventa logotipos, capturas de tela e música |
| `<direction>` | Define a linguagem visual: o que se transforma em quê, cores, letras, câmera e o que não pode aparecer | O resultado vira um “PowerPoint animado” com transições |
| `<truth>` | Registra o que seu produto faz DE VERDADE, com os textos exatos da interface | Aparecem funções que não existem |
| `<structure>` | Define o roteiro por pulsos da música: o que acontece em cada trecho | O ritmo fica monótono e tudo dura o mesmo tempo |
| `<build>` | Explica como montar o filme por dentro (Claude lê, você não) | Surgem saltos, piscadas e áudio fora de sincronia |
| `<gotchas>` | Reúne armadilhas conhecidas do navegador e regras da sua marca | Erros que já custaram horas voltam a acontecer |
| `<start>` | Exige a apresentação de uma prévia antes da produção | Você recebe dois minutos de vídeo que não queria |

---

## O modelo

```text
<inputs>
Peça:
- o formato: vertical 1080×1920 para reels e anúncios (recomendado) ou horizontal 1920×1080 para web ou YouTube;
- o wordmark em uma palavra (recomendado: [um verbo ou palavra curta que resuma o que o produto faz, com ponto final: «atende.», «fatura.», «publica.»]);
- de 6 a 10 capturas de tela reais de [produto] ([quais telas]); se não houver, recrie a interface em HTML com os textos e as cores reais abaixo;
- [meu logo / o kit de marca de uma ferramenta que apareça no vídeo, somente se eu tiver permissão para usá-lo];
- uma faixa livre de direitos autorais, com cerca de 120 BPM e pelo menos [duração + 10 s], com um drop e um breakdown tranquilo (Mixkit, uso comercial gratuito);
- um clipe gratuito de banco de vídeos de [uma cena do mundo real em que o resultado fique claro: um balcão no escuro, uma mesa cheia de papéis, uma loja fechada…] (Pexels).
</inputs>

<direction>
Filme de lançamento no estilo de uma apresentação da Apple, somente em 2D e em um único plano contínuo: cada cena nasce da anterior, sem transições, desfoques nem cortes. Os elementos se transformam uns nos outros. Os textos sobem de uma linha de máscara, os ícones surgem do nada com efeito de mola, as barras são desenhadas de um lado ao outro, as páginas avançam e uma forma [preta / da sua cor escura] preenche a tela antes de encolher na cena seguinte.
[Se o filme precisa EXPLICAR, e não apenas mostrar: «Quem assistir uma vez deve conseguir explicar o que o produto faz. No topo há um trilho com [3-4] etapas que se preenche conforme o filme avança: [Etapa 1 · Etapa 2 · Etapa 3 · Etapa 4]. Cada número exibido corresponde aos demais.»]
Cada função aparece com um título curto que sobe da máscara (2 a 4 palavras, [tipografia] 800), explica o que acontece na tela e se transforma no próximo elemento, sem transição.
Paleta: fundo [#color], interface em [#color], destaque [#color] somente para [badges, confirmações e o ponto do wordmark], estado de alerta [#color]. Liquid glass do iOS 26 sobre a interface e o vídeo. Tipografias: [uma com bastante personalidade] para o wordmark, [uma limpa] para a interface e [uma monoespaçada] para horários, valores e dados.
Um cursor dispara cada mudança com cliques, arrastes e pressionamentos longos reais. A câmera aplica zoom no estilo do Screen Studio para preencher o enquadramento a cada momento, e o cursor acompanha o zoom.
Proibido: transições encadeadas, entradas com desfoque, “revelações” com brilho, giros 3D, partículas, brilhos decorativos, pausas com mais de 1 s e qualquer coisa com cara de modelo pronto.
</direction>

<truth>
Somente funções reais de [produto]:
- [função 1];
- [função 2];
- [função 3 …];
Textos exatos da interface: «[texto exato 1]», «[texto exato 2]», «[texto exato 3]».
Dados fictícios ([nome de empresa inventada], [pessoas inventadas]). Nenhum cliente real nem dado pessoal. Sem URL. Chamada para ação final: «[CTA exata]».
[Regras próprias de veracidade: «o assistente nunca aparece aprovando um pagamento», «o preço não aparece na tela»…]
</truth>

<structure>
120 BPM, [N] pulsos ([duração]), com algo acontecendo a cada pulso. [Formato]; toda a ação dentro da área segura (no formato vertical, deixe livres os 220 px de cima e os 380 px de baixo). Ajuste os limites de cada trecho aos tempos medidos da faixa: o drop, o breakdown e a volta do ritmo definem o tempo.

1 · Abertura (pulsos 1-16): [o wordmark se comprime dentro do próprio ponto; o ponto se expande em uma pílula e, dentro dela, sobe «[a situação inicial, com horário ou número]»]. [Algo que seja contado ou acumulado, um pulso de cada vez].
2 · [Nome do trecho] (17-24): [qual ação do cursor provoca qual mudança]. Termine com um zoom que chegue exatamente no DROP.
3 · [Função principal] (25-56): [mensagem ou solicitação recebida] → [o que o produto faz, com o texto exato da interface] → [resultado visível ✓].
4 · [Função] ([pulsos]): […]
5 · [Função] ([pulsos]): […]
6 · [Função] ([pulsos]): […]
[…]
N-2 · Com controle ([pulsos]): uma única forma que continua se transformando: [garantia 1 ✓] → [garantia 2 ✓] → [garantia 3 ✓].
N-1 · Mundo real ([pulsos], no BREAKDOWN): o círculo se expande até preencher a tela, fica assim por um pulso e encolhe sobre o clipe real. Uma íris se abre sobre [a tela do celular / o resultado] e os contadores surgem, um por pulso: «[resumo do resultado com números]».
N · Encerramento ([pulsos], com a VOLTA do ritmo): tudo se contrai até virar uma pílula, depois um ponto, e as letras do wordmark voltam a surgir. Abaixo, aparece «[CTA]». O último quadro é igual ao primeiro (exceto por essa linha).
</structure>

<build>
1. Um único HTML de [largura×altura]. Tudo é calculado a partir do tempo dentro de um async seek(t): sem transições CSS, sem temporizadores e sem estado que passe de um quadro para outro. Exponha window.videoSpec e window.renderReady.
2. Molas com fórmula fechada. Se um valor mudar de objetivo várias vezes, some uma mola para cada mudança, para que o resultado continue sendo uma função do tempo. Faça o mesmo com os contadores.
3. Liquid glass: cada cristal contém uma cópia da cena atrás dele, deformada por um mapa de deslocamento SVG (feImage com o campo de distância de um retângulo arredondado) em três feDisplacementMap com escalas ligeiramente diferentes, para separar as cores nas bordas, e mais uma luz de borda. Para letras de cristal, crie um campo de distância por letra no canvas.
4. Efeito gota (goo): aplique desfoque e um limite de alfa, com o original por cima para manter o cristal nítido.
5. Íris com 6 lâminas em torno de uma abertura hexagonal.
6. Vídeo de banco: recodificado totalmente em intra (ffmpeg -g 1), carregado como blob URL e aguardando «seeked» a cada quadro.
7. Som: um efeito baixado (Mixkit) por evento, posicionado pelo pico medido.
   - Uma lista única de eventos (tempo, tipo) serve de base para a animação e os efeitos.
   - A música começa no tempo forte; o primeiro grande zoom coincide com o drop, o mundo real aparece no breakdown e o wordmark volta com o ritmo.
   - Se a faixa for curta, prolongue-a repetindo frases completas de 8 compassos, nunca no meio da frase.
   - Normalize para −14 LUFS.
8. Renderize com Playwright a 60 fps, combinando 4 subquadros por quadro. Confira um quadro por pulso e procure saltos de um único quadro.
</build>

<gotchas>
- backdrop-filter: url() não aplica direito os mapas de deslocamento no Chromium: clone a cena.
- Uma inundação de cor precisa avançar a partir dos cantos e durar cerca de 0,3 s.
- Um elemento filho com visibility: visible aparece através de um elemento pai oculto: use inherit.
- O texto que muda dentro de uma forma em transformação precisa da própria máscara.
- O Chrome varia a suavização de texto entre duas capturas iguais: compare os quadros com tolerância, não byte a byte.
- Valores e horários precisam de fonte monoespaçada ou números tabulares para não ficarem pulando.
- Revise o clipe de banco inteiro: pode haver textos ou marcas que você não quer.
- [Regras da sua marca: «o logo da [ferramenta] só aparece no selo de parceiro», «nenhum quadro pode mostrar dados de um cliente»…]
</gotchas>

<start>
Peça os materiais e depois me mostre o mapa de pulsos e [4-6] quadros ([abertura], [função principal], [outra função], [mundo real]) antes de escrever o filme inteiro.
</start>
```

---

## Dicas para preencher

- **Os pulsos são o roteiro.** A 120 BPM, 2 pulsos = 1 segundo. 112 pulsos ≈ 56 s (redes sociais); 192 pulsos ≈ 1:36 (para mostrar tudo).
- **Escreva ações, não telas.** Ruim: «tela de agenda». Bom: «o cursor arrasta o compromisso de quinta para sexta e aparece «Compromisso remarcado ✓»».
- **Um fio condutor.** Algo que aparece no início e no fim: o ponto do wordmark, uma pílula, um celular.
- **O bloco `<truth>` é indispensável.** Inclua os textos exatos da sua interface. Isso faz o vídeo parecer seu produto, e não um produto genérico.
- **Você não precisa entender `<build>`.** Deixe como está: é para Claude.
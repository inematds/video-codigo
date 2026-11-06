# Exemplo completo · Filme que EXPLICA

A mesma estrutura do `03`, mas pensada para que quem assista **uma única vez consiga contar o que o produto faz**. Produto **fictício**: um assistente que prepara faturas por chat, lê as faturas de fornecedores recebidas por e-mail e transforma a foto de um recibo em uma despesa. É baseado em um filme real de 1:37, com produto, marcas e dados alterados.

**O que acrescenta em relação ao `03`** (copie para seus prompts quando o vídeo precisar vender um serviço, não apenas impressionar):

- **Uma trilha de 4 etapas** no alto, que avança junto com o vídeo: Você pede · Você revisa · Chega até você · Você fica sabendo. O espectador sempre sabe em que parte está.
- **Números que fecham.** Base + IVA = total; a soma das faixas = o valor pendente. Se algum número não fechar, alguém percebe.
- **O que NÃO faz**, escrito em `<truth>`. Assim, nenhum quadro promete demais.
- **O gancho no quadro 0**: o caos (documentos acumulados) e a marca aparecem antes dos 4 segundos, com o drop bem nesse momento.

---

```text
<inputs>
Peça-me:
- o formato: vertical 1080×1920 para anúncios e reels (recomendado) ou horizontal 1920×1080 para a web;
- o wordmark em uma palavra (recomendado: «factura.», que pode ser verbo e substantivo);
- 6-10 capturas reais: o chat preparando uma fatura, o rascunho no programa de faturamento (conta de testes, nunca dados de clientes), a caixa de entrada com as etiquetas Facturas/* e a foto de um recibo convertida em despesa (se não houver, recrie a interface em HTML com os textos e as cores abaixo);
- uma faixa livre de direitos autorais, com cerca de 120 BPM e pelo menos 1:50, com drop e um breakdown tranquilo (Mixkit, uso comercial gratuito);
- um clipe gratuito de banco de imagens de uma mesa escura à noite, com papéis e recibos empilhados e um celular que acende sobre a mesa (Pexels).
</inputs>

<direction>
Filme de lançamento no estilo de uma keynote da Apple, apenas em 2D e em um único plano contínuo: cada cena surge da anterior, sem fusões, desfoques ou cortes. Os elementos se transformam uns nos outros. Os textos sobem por uma linha de máscara, os ícones surgem do zero com efeito de mola, as barras e as linhas da fatura são desenhadas de um lado ao outro, as páginas avançam e uma forma de tinta preenche a tela antes de encolher na cena seguinte.
Precisa EXPLICAR, não apenas impressionar: quem assistir uma vez deve conseguir contar o que o produto faz. Para isso:
- No alto, dentro da área segura, há uma trilha de 4 etapas que avança junto com o vídeo: Você pede · Você revisa · Chega até você · Você fica sabendo. A etapa ativa recebe a cor de destaque.
- Cada número exibido fecha com os demais (base + IVA = total; a soma das faixas = o valor pendente).
- Cada função é apresentada com um título curto que sobe pela máscara (2-4 palavras, Geist 800), explica o que acontece na tela e se transforma no próximo elemento, nunca por fusão.
Paleta: fundo papel #F6F4EE, cartões #FFFFFF, interface em tinta #14161A, texto secundário #6B6F76 e bordas #E4E1D8. Azul elétrico #3B5BFF apenas nos badges, nas confirmações, no ponto do wordmark e na etapa ativa da trilha. Alerta em #C2185B sobre #FDECF2 (duplicidade bloqueada, IVA inválido). Liquid glass do iOS 26 sobre a interface e o vídeo. Bricolage Grotesque 800 para o wordmark, Geist para a interface e Geist Mono para valores, datas e dados.
Um cursor dispara cada mudança com cliques, arrastes e pressões longas reais. A câmera aproxima no estilo do Screen Studio para cada momento preencher o enquadramento, e o cursor acompanha a escala.
Proibido: fusões encadeadas, entradas com desfoque, «revelações» com brilho, linhas de varredura brilhantes, giros 3D, partículas, brilhos, pausas com mais de 1 s e qualquer elemento com cara de template.
</direction>

<truth>
O serviço: um assistente que prepara faturas por chat + faturas de fornecedores recebidas por e-mail + recibos fotografados, tudo dentro do programa de faturamento do cliente. Apenas funções reais:
- O assistente busca o cliente, prepara a fatura de venda EM RASCUNHO, consulta o que foi faturado em um período e o que está pendente de recebimento por tempo de atraso.
- Se houver vários clientes com nomes compatíveis, ele os mostra e pergunta; não escolhe sozinho.
- Pede confirmação antes de preparar a fatura.
- NUNCA aprova uma fatura: uma pessoa assina a emissão definitiva.
- Validações no código, não na IA: valores positivos, IVA somente de 21, 10, 4 ou 0 % e datas válidas.
- Se a mesma fatura for solicitada duas vezes, não cria outra.
- Faturas de fornecedores por e-mail: a mensagem chega, a IA lê o PDF, cadastra o fornecedor se ele ainda não existir e deixa a compra em rascunho com o PDF anexado. O e-mail passa de «Facturas/Pendiente» para «Facturas/Procesado»; se não for uma fatura, vai para «Facturas/NoFactura». Reenviar a mesma mensagem não duplica nada.
- Recibos: foto ou PDF do recibo → despesa em rascunho com a imagem anexada.
NÃO mostrar: que o assistente aprove ou envie faturas, cobre clientes ou faça aprovações automáticas.
Chips do filme: «Buscando cliente», «Rascunho pronto», «Sem duplicidades», «IVA validado», «PDF anexado», «Pendente de recebimento».
Dados fictícios: empresa «Estudio Lince» (estúdio de design); clientes «Panadería Roble, S.L.» e «Roble Hermanos, C.B.»; fornecedor «Imprenta Faro». Nenhum cliente real. Sem URL. Chamada final para ação: «Peça sua demo».
</truth>

<structure>
120 BPM, 176 batidas (1:28), com algo acontecendo em cada batida. Vertical 1080×1920; toda a ação dentro da área segura (deixe livres os 220 px de cima e os 380 px de baixo; a trilha de etapas fica logo abaixo dos 220 px). Ajuste os limites de cada trecho aos tempos medidos da faixa: o drop, o breakdown e a volta do ritmo ditam o andamento.

1 · Gancho (batidas 1-8): quadro 0 = caos: uma pilha de documentos (faturas, PDFs, recibos) e o título «À mão, de novo.». Um contador de pendências sobe até 29. A pilha é absorvida pelo ponto do wordmark e o contador cai para «0 por fazer» bem quando entra o DROP (antes dos 4 s): aparece «factura.».

2 · Tudo entra em um só lugar (9-24): o ponto se expande em uma cápsula de tinta com «Dia 30 · 19:48 · fechamento do mês». Clique: seis lâminas de íris se fecham sobre a cápsula e se abrem de repente sobre a lista de vendas. Atrás dela, surge uma grade como um mapa de papel: o programa de faturamento no centro e, ao redor, chat, e-mail, foto de recibo, PDF, contatos, IVA, rascunho e recebimentos. Os elementos se reorganizam em mosaico e um clique aproxima o chat. A trilha acende «Você pede».

3 · Peça pelo chat (25-56): chega «Fatura para Panadería Roble: 1.000 € + IVA pelo design das etiquetas». Surge «Buscando cliente» e aparecem dois candidatos (Panadería Roble, S.L. · Roble Hermanos, C.B.). Sobe a pergunta «Qual dos dois?». O cursor toca em S.L.
O chip derrete em uma gota que se estica até formar uma barra de cristal com as 4 funções (Cliente · Fatura · Faturado · Pendente). O ícone Fatura se abre em uma fatura cujas linhas são desenhadas uma por batida: Design das etiquetas · Base 1.000,00 € · IVA 21 % 210,00 € · Total 1.210,00 €. O assistente pergunta «Posso preparar?». Pressão longa em «Sim»: a fatura voa para a lista e pousa com «Rascunho pronto ✓».
Um cursor fantasma envia a mesma mensagem de novo e bate em um cadeado: «Já existe · sem duplicidades».

4 · Você aprova (57-72): a trilha avança para «Você revisa». Uma lupa de cristal se posiciona sobre o campo IVA. Alguém digita 18 %: o campo treme em cor de alerta e surge «IVA válido: 21 · 10 · 4 · 0»; volta para 21 % e aparece «IVA validado ✓». Surge um cadeado ao lado do assistente: «Nunca aprova». O cursor humano clica em «Aprovar»; título: «Assinado por uma pessoa».

5 · Chegam por e-mail (73-96): a trilha avança para «Chega até você». A fatura aprovada se dobra em um envelope que voa para a caixa de entrada; a etiqueta «Facturas/Pendiente» é desenhada de um lado ao outro. Abre-se o e-mail da Imprenta Faro com seu PDF. A lupa percorre o documento e sublinha cada dado, um por batida: NIF · Base 300,00 € · IVA 21 % · Total 363,00 €. Os dados voam para o formulário de compra, o PDF se prende como um clipe («PDF anexado ✓») e aparece «Rascunho pronto ✓». A etiqueta desliza para «Facturas/Procesado». Um segundo e-mail, um boletim sem fatura, desliza sozinho para «Facturas/NoFactura».

6 · Recibo: uma foto (97-108): a etiqueta se estica até formar o visor da câmera do celular. O obturador aponta para um recibo de posto de gasolina (45,60 €). A foto vira e se transforma em uma despesa em rascunho com a imagem anexada.

7 · Quem ainda precisa pagar? (109-132): a trilha avança para «Você fica sabendo». O visor encolhe e vira o chat. Pergunta: «O que tenho pendente de receber?». Surge «Pendente de recebimento» e as barras são desenhadas por tempo de atraso: 0-30 dias 2.140 € · 31-60 dias 980 € · mais de 60 dias 360 €. Abaixo sobe «4 faturas · 3.480 €». Segunda pergunta: «Quanto faturei neste trimestre?». Um contador em Geist Mono gira até 18.450 € e surge uma barra por mês.

8 · Com controle (133-144): uma única forma de tinta que não para de se transformar: Nunca aprova ✓ → Se tiver dúvida, pergunta ✓ → Sem duplicidades ✓ → IVA validado ✓ → Cada despesa com seu PDF ✓.

9 · Mundo real (145-168, no BREAKDOWN): o círculo final se expande até a tinta preencher a tela, permanece por uma batida e encolhe sobre o clipe real da mesa escura, com o celular acendendo. A mesma íris se abre sobre a tela do celular e os contadores surgem um por batida: «Este mês: 12 faturas preparadas · 23 despesas com seus PDFs · 0 digitadas à mão · 1 clique para aprovar», e fecha de novo.

10 · Encerramento (169-176, com a VOLTA do ritmo): tudo se contrai na cápsula, depois no ponto, e as letras de «factura.» surgem de novo na batida de retorno. Abaixo sobe «Peça sua demo». O último quadro é igual ao primeiro (exceto por essa linha e pela trilha completa).
</structure>

<build>
1. Um único HTML vertical de 1080×1920. Tudo é calculado a partir do tempo dentro de um async seek(t): sem transições CSS, sem temporizadores e sem estado que passe de um quadro para outro. Exponha window.videoSpec e window.renderReady.
2. Molas com fórmula fechada. Se um valor mudar de objetivo várias vezes, some uma mola para cada mudança para que ele continue sendo função do tempo. Os contadores (pendências, 18.450 €, os do mundo real) também.
3. Liquid glass: cada cristal leva uma cópia da cena que está atrás dele, deformada com um mapa de deslocamento SVG (feImage com o campo de distância de um retângulo arredondado) em três feDisplacementMap com escalas um pouco diferentes, mais uma luz de borda.
4. Efeito gota (goo): desfoque mais limite de alfa, com o original por cima para manter o cristal nítido.
5. Íris de 6 lâminas ao redor de uma abertura hexagonal.
6. Compressão do wordmark: cada letra se aproxima do ponto na mesma proporção e fica mais estreita para continuar encostando na letra seguinte. Se a tipografia não tiver eixo de largura, estreite com scaleX por letra e, abaixo de 0,6, reduza o peso.
7. Vídeo de banco de imagens: recodificado totalmente como intra (ffmpeg -g 1), carregado como blob URL e esperando por «seeked» em cada quadro.
8. Som: um efeito baixado (Mixkit) por evento, posicionado conforme o pico medido.
   - Uma única lista de eventos (tempo, tipo) que alimenta a animação e os efeitos.
   - Meça o BPM real da faixa antes de definir as batidas («cerca de 120» pode ser 129,8) e edite a música para o drop cair no gancho.
   - O mundo real acontece no breakdown e o wordmark volta junto com o ritmo.
   - Se a faixa for curta, estenda repetindo frases inteiras de 8 compassos, nunca no meio de uma frase.
   - Normalize para −14 LUFS.
9. Renderize com Playwright a 60 fps, misturando 4 subquadros por quadro, em paralelo com poucos processos. Revise um quadro por batida e procure saltos de um único quadro.
</build>

<gotchas>
- backdrop-filter: url() não aplica bem os mapas de deslocamento no Chromium: faça uma cópia da cena.
- Uma inundação de cor precisa vir dos cantos e durar cerca de 0,3 s.
- Um elemento filho com visibility: visible aparece através de um elemento pai oculto: use inherit.
- O texto que muda dentro de uma forma em transformação precisa da própria máscara.
- O Chrome varia a suavização do texto entre duas capturas iguais: compare quadros com tolerância, não byte a byte.
- Valores no formato espanhol (1.210,00 €) e em Geist Mono com algarismos tabulares, para não pularem durante a rolagem.
- Nunca mostre um quadro em que o assistente apareça aprovando ou enviando uma fatura.
- Revise o clipe de banco de imagens inteiro: pode haver textos ou notificações em inglês que contradigam a mensagem; se houver, cubra-os ou troque o clipe.
</gotchas>

<start>
Peça-me os materiais e depois mostre o mapa de batidas e 6 quadros (gancho, peça pelo chat, você aprova, chegam por e-mail, quem ainda precisa pagar, mundo real) antes de escrever o filme completo.
</start>
```
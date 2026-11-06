# Exemplo completo · Filme de lançamento

O modelo `02` preenchido para um produto **fictício**: uma recepcionista com IA que atende os clientes de um negócio por chat enquanto ele está fechado. Baseia-se em um filme real de 1:36, com o produto, as marcas e os dados alterados.

**Use assim:** troque o produto pelo seu (ou peça ao Claude: «adapte este prompt ao meu produto com o que você sabe sobre ele»), revise linha a linha o bloco `<truth>` e cole-o em uma conversa nova.

**Por que funciona:**
- Conta uma história (uma noite na recepção, das 23:47 até de manhã), em vez de listar funções.
- Cada função é uma ação do cursor com seu resultado: «Consulta reservada ✓».
- A música cai no primeiro grande zoom, e o breakdown acontece no «mundo real».
- O último quadro é igual ao primeiro: o vídeo entra em loop nas redes.

---

```text
<inputs>
Peça-me: o wordmark em uma só palavra (recomendação: «atende.», que é um verbo e diz o que faz); de 6 a 10 capturas reais da demonstração e do painel de contatos (se não houver, recrie a interface em HTML com os textos e as cores abaixo); uma faixa livre de direitos autorais de cerca de 120 BPM e pelo menos 1:30, com drop e breakdown tranquilo (Mixkit, uso comercial gratuito); e um clipe gratuito de banco de imagens com um balcão de recepção escuro à noite e um celular aceso sobre a mesa (Pexels).
</inputs>

<direction>
Filme de lançamento no estilo de uma apresentação da Apple, apenas em 2D e em um único plano contínuo: cada cena nasce da anterior, sem dissoluções, desfoques nem cortes. Os elementos se transformam uns nos outros. Os textos sobem de uma linha de máscara, os ícones surgem do zero com efeito de mola, as barras são desenhadas de um lado ao outro, as páginas avançam e uma forma preta preenche a tela antes de encolher na cena seguinte.
Fundo branco quente (#FAFAF7), interface em preto-tinta (#0A0A0A) e um único destaque em laranja-mandarina (#FF6A2B), usado apenas em badges, confirmações e no ponto do wordmark. Liquid glass do iOS 26 na interface e no vídeo. Archivo (largura 125, peso 800) para o wordmark, Inter Tight para a interface e JetBrains Mono para horários e dados.
Um cursor dispara cada mudança com cliques, arrastes e pressionamentos longos reais. A câmera aproxima no estilo Screen Studio para que cada momento ocupe o enquadramento vertical, e o cursor aumenta junto.
Cada função é apresentada com um título curto que sobe da máscara (2 a 4 palavras, Inter Tight 800) e se transforma no elemento seguinte, nunca com uma dissolução.
Proibido: dissoluções encadeadas, entradas com desfoque, «revelações» com brilho, giros 3D, partículas, brilhos, pausas de mais de 1 s e qualquer coisa com cara de modelo pronto.
</direction>

<truth>
Somente funções reais da recepcionista:
- responde com informações do negócio (horários, preços, serviços);
- consulta horários disponíveis e marca, altera ou cancela consultas (uma consulta por horário);
- entende mensagens de voz;
- inclui na lista de espera quando não há horário disponível;
- responde no idioma de quem escreve;
- encaminha urgências para uma pessoa, com um resumo, e entra em pausa;
- salva o contato no CRM sem duplicá-lo;
- canais: web, Instagram e email;
- cada ação fica registrada.
Rótulos literais da interface: «Consulta de informações», «Horário verificado», «Consulta reservada», «Consulta alterada», «Contato salvo», «Na lista de espera», «Encaminhado para uma pessoa».
Dados fictícios: Clínica Veterinária Olivo, animais «Kira» e «Bruno». Nenhum cliente real nem dado pessoal. Sem URL. Chamada para ação final: «Peça uma demonstração».
</truth>

<structure>
120 BPM, 160 batidas (1:20), com algo acontecendo em cada batida. Vertical 1080×1920; toda a ação dentro da área segura (deixe livres os 220 px de cima e os 380 px de baixo). Ajuste os limites de cada trecho aos tempos medidos da faixa: o drop, o breakdown e a volta do ritmo determinam o andamento.

1 · Abertura (batidas 1-16): o wordmark «atende.» se comprime como um acordeão dentro do próprio ponto. O ponto se expande em uma pílula preta e, dentro dela, surge «23:47 · recepção fechada». Sobre a pílula, aparece um badge que conta mensagens, uma por batida (1→6), cada uma com o ícone do canal surgindo.

2 · Canais (17-24): clique: seis lâminas de íris se fecham sobre o rótulo e se abrem de repente sobre uma conversa. O círculo vira um cartão de chat e encolhe. Atrás dele, abre-se uma grade como um mapa de papel (centro, cruz, cantos): web, Instagram, email, agenda e CRM. A grade se reorganiza em mosaico e um clique aproxima a tela do Instagram, chegando bem no DROP.

3 · Responde e agenda (25-56): chega «Vocês têm horário amanhã para vacinar a Kira?». Surge o chip «Consulta de informações» e a resposta com o preço sobe da máscara. O chip derrete em uma gota que se alonga até formar uma barra de ferramentas de cristal (informações, agenda, CRM, pessoa). O ícone da agenda transforma a barra em um controle deslizante de horários (16:30 · 17:15 · 18:00). Ao arrastar, o botão mantido sob o cursor vira uma lupa de cristal sobre 17:15. Ao soltar: «Consulta reservada ✓». Um segundo cursor fantasma tenta selecionar o mesmo horário e rebate em um cadeado: «Um horário, uma consulta».

4 · Entende áudios (57-72): a lupa sobe como um orbe de cristal e cresce até virar uma tela de bloqueio com um relógio de cristal (00:32). A barra inicial se alonga e vira um reprodutor de mensagem de voz: a onda pulsa no ritmo e se transforma em texto que sobe da máscara («Você pode passar a consulta do Bruno para sexta-feira?»). O cartão é arrastado de QUI para SEX: «Consulta alterada ✓».

5 · Idiomas e lista de espera (73-88): o relógio se dissolve em uma bolha de cristal onde a palavra muda letra por letra a cada batida: Hola → Hi! → Ciao. A bolha cai sobre a linha «Sábado», que se enche de preto até mostrar «Lotado». O cursor clica em «Avise-me» e uma ficha sobe para a lista de espera com um contador que salta para +1: «Na lista de espera ✓».

6 · Sabe quando parar (89-100): a ficha se alonga e vira uma mensagem urgente («Meu cachorro comeu uvas»). A borda da forma preta fica vermelha (#E5383B) e surge «Encaminhado para uma pessoa». Um cartão de resumo se abre como um acordeão, e um interruptor de cristal coloca a assistente «Em pausa».

7 · Seu CRM (101-124): a cena recua e revela um celular; a moldura cresce a partir da borda da tela. A Dynamic Island se alonga como um líquido, se separa, atravessa a tela voando e se expande em uma janela de computador com o CRM. Pressionamento longo sobre a conversa e arraste até a janela: ao soltar, ela vira a ficha do contato. Os campos são desenhados um por batida: Interesse · Canal · Status: interessado; depois «Sem duplicados ✓». Rolagem: a ficha se transforma no registro de atividade, e cada linha surge com seu rótulo e horário.

8 · Com controle (125-136): uma única forma preta que não para de se transformar: Confirma antes de agir ✓ → Uma consulta por horário ✓ → Tudo fica registrado ✓ → Ativo 24/7 ✓.

9 · Mundo real (137-152, no BREAKDOWN): o círculo final se expande até o preto preencher a tela, permanece por uma batida e encolhe sobre o clipe real do balcão escuro, com o celular se acendendo. A mesma íris se abre sobre a tela do celular, e os contadores surgem um por batida: «Enquanto você dormia: 6 conversas · 2 consultas · 1 na espera · 1 urgência atendida», e volta a se fechar.

10 · Encerramento (153-160, com a VOLTA do ritmo): tudo se contrai em uma pílula, depois no ponto, e as letras de «atende.» voltam a surgir na batida de retorno. Abaixo, aparece «Peça sua demonstração». O último quadro é igual ao primeiro (exceto por essa linha).
</structure>

<build>
1. Um único HTML vertical de 1080×1920. Tudo é calculado a partir do tempo dentro de um async seek(t): sem transições CSS, sem temporizadores e sem estado que passe de um quadro para outro. Exponha window.videoSpec e window.renderReady.
2. Molas com fórmula fechada. Se um valor mudar de objetivo várias vezes, some uma mola para cada mudança, para que continue sendo função do tempo. Os contadores também.
3. Liquid glass: cada elemento de cristal leva uma cópia da cena atrás dele, deformada por um mapa de deslocamento SVG (feImage com o campo de distância de um retângulo arredondado) em três feDisplacementMap com escalas ligeiramente diferentes, além de uma luz de borda. Para o relógio de cristal, use um campo de distância por algarismo feito em canvas.
4. Efeito de gota (goo): desfoque mais limiar de alfa, com o original por cima para que o cristal continue nítido.
5. Íris de 6 lâminas ao redor de uma abertura hexagonal.
6. Compressão do wordmark: cada letra se aproxima do ponto na mesma proporção e se estreita para continuar encostando na seguinte.
7. Vídeo de banco de imagens: recodificado totalmente como intra (ffmpeg -g 1), carregado como blob URL e aguardando «seeked» em cada quadro.
8. Som: um efeito baixado (Mixkit) por evento, colocado de acordo com seu pico medido.
   - Uma lista única de eventos (tempo, tipo), da qual saem a animação e os efeitos ao mesmo tempo.
   - A música começa em um tempo forte; a aproximação ao Instagram cai no drop, o mundo real no breakdown e o wordmark volta com o ritmo.
   - Se a faixa for curta, ela é prolongada repetindo frases completas de 8 compassos, nunca no meio de uma frase.
   - Normalize para −14 LUFS.
9. Renderize com Playwright a 60 fps, misturando 4 subquadros por quadro. Revise um quadro por batida e procure saltos de um único quadro.
</build>

<gotchas>
- backdrop-filter: url() não aplica bem os mapas de deslocamento no Chromium: clone a cena.
- Uma inundação de cor precisa partir dos cantos e durar cerca de 0,3 s.
- Um filho com visibility: visible aparece através de um elemento pai oculto: use inherit.
- O texto que muda dentro de uma forma que se transforma precisa da própria máscara.
- O Chrome varia a suavização do texto entre duas capturas iguais: compare quadros com tolerância, não byte a byte.
- Horários e contadores em JetBrains Mono, para que não fiquem pulando.
- Os ícones dos canais são simplificados, não são logos oficiais.
</gotchas>

<start>
Peça-me os inputs e depois mostre o mapa de batidas e 6 quadros (abertura, responde e agenda, entende áudios, seu CRM, com controle, mundo real) antes de escrever o filme inteiro.
</start>
```
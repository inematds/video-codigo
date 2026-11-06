# Prompt de filme

Formato para entregar um briefing completo que outra conversa consiga produzir sem contexto prévio. Serve para filmes de lançamento, demonstrações e explicações de produto. Ao adaptar um existente, mantenha a estrutura e substitua todo o conteúdo. Não reutilize marcas, dados nem recursos do original.

## Blocos

| Bloco | Conteúdo obrigatório |
| --- | --- |
| `<inputs>` | O que pedir antes de começar: formato, wordmark, capturas reais, faixa (BPM aproximado, duração mínima, drop e breakdown), clipe de banco de imagens e licença. Oferecer a recriação da interface se não houver capturas. |
| `<direction>` | Linguagem visual: plano contínuo ou cortes, o que se transforma em quê, paleta com códigos, tipografias com peso, câmera, cursor, títulos e lista de proibições. |
| `<truth>` | Funções reais e rótulos literais da interface, dados fictícios identificados como tal, nada de clientes reais, CTA exata. Este bloco impede invenções. |
| `<structure>` | BPM, número de batidas e duração; formato e área segura; trechos numerados com seus intervalos de batidas e a ação visível em cada um. Marcar onde entram o drop, o breakdown e a volta do ritmo. |
| `<build>` | Contrato técnico: um HTML, `seek(t)` puro, `window.videoSpec` e `window.renderReady`, molas em formato fechado, técnica de cada efeito, som a partir de uma lista única de eventos, renderização e revisão. |
| `<gotchas>` | Falhas conhecidas do navegador e dos materiais, e regras de veracidade específicas do briefing. |
| `<start>` | Etapa de aprovação: pedir os materiais e mostrar o mapa de batidas e 4–6 quadros-chave antes de escrever o filme inteiro. |

## Regras que deram bons resultados

- Descreva cada trecho como uma ação com causa e consequência («o cursor arrasta o compromisso de QUA para SEX: “Compromisso remarcado ✓”»), não como uma tela.
- Um objeto persistente atravessa o filme: o ponto do wordmark, uma pílula preta, um orbe. O último quadro repete o primeiro.
- Duração conforme o conteúdo: 50–60 s para redes sociais; 90–110 s se for preciso mostrar tudo o que o produto faz. Ajuste os limites dos trechos aos tempos medidos da faixa.
- Se a peça precisar explicar, acrescente uma trilha de 3–4 etapas que se preenche ao longo do filme e títulos de 2–4 palavras que descrevam o que acontece na tela.
- Os números na tela devem fechar entre si (base + impostos = total; a soma dos trechos = o valor pendente) e variar conforme o tempo.
- O gancho de 0–3 s mostra o problema ou a marca no quadro 0; o drop da música acompanha a primeira revelação.
- Meça o BPM real da faixa antes de definir as batidas: «cerca de 120» pode ser 129,8.
- Edite a música somente nos limites das frases musicais (8 compassos), nunca no meio de uma frase.

## Avisos técnicos

- `backdrop-filter: url()` não aplica bem mapas de deslocamento no Chromium. Para criar o efeito de vidro, clone a cena de trás e aplique o filtro ao clone.
- Uma inundação de cor precisa ultrapassar os cantos e durar cerca de 0,3 s. Caso contrário, metade da tela muda em um quadro.
- `visibility: visible` em um elemento filho aparece através de um elemento pai oculto. Use `inherit`.
- O texto que muda dentro de uma forma em transformação precisa de uma máscara própria.
- Vídeo dentro do HTML: recodifique tudo em modo intra (`ffmpeg -g 1`), carregue como blob URL e espere o evento `seeked` antes de desenhar. Um servidor sem solicitações por intervalos não permite buscar quadros.
- Uma tipografia sem eixo `wdth` fica mais estreita com `scaleX` em cada letra. Abaixo de 0,6, compense reduzindo o peso.
- Use fonte monoespaçada ou tabular para as cifras, para que não saltem durante a rolagem.
- Revise os clipes de banco de imagens quadro a quadro. Eles podem conter textos, marcas ou notificações que contradizem a mensagem.
- Renderize em paralelo com poucos processos. Com processos demais, um deles pode travar ao carregar o vídeo.

## Entrega do prompt

Entregue o prompt inteiro em um único bloco de texto, seguido de uma lista breve do que mudou em relação ao original e do que a outra conversa precisa (faixa, clipe, efeitos ou permissão para buscá-los). Salve-o no projeto como fonte da produção.
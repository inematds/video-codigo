# Prompts rápidos

São prompts usados em produções reais com esta skill. Só trocamos nomes de produtos e marcas por `[colchetes]`. Copie, preencha os colchetes e cole na aba **Code** do Claude, com a sessão aberta na pasta do seu projeto.

Não precisa escrever bem nem usar termos técnicos: a skill faz as perguntas que faltam e mostra um teste antes do vídeo longo.

---

## 1 · Mostre o material primeiro

Antes de pedir o vídeo, peça para o Claude ler tudo o que há sobre o que você quer mostrar. Quanto mais real for o material, menos ele inventa.

```text
Busque todas as informações que você tem sobre [produto] em [repositório do GitHub / esta pasta / este site / Notion / Drive]. Resuma o que ele realmente faz, para quem serve e o que dá para mostrar na tela.
```

---

## 2 · O primeiro vídeo (longo, que explique tudo)

```text
Com todas as informações que você tem sobre [produto], use a skill criar-videos-con-codigo para gerar o melhor vídeo possível. Ele precisa ser longo e explicar tudo o que o produto faz. Também precisa ter som.
```

---

## 3 · A versão para redes (vertical, bem dinâmica)

Este foi o prompt que melhor funcionou para transformar um «vídeo explicativo» em um «vídeo que faz parar de rolar a tela». Repare em três coisas: a sincronia do som, a duração máxima e os 3 primeiros segundos.

```text
Agora faça outro vídeo, bem mais dinâmico e na vertical, para redes sociais. Ele precisa chamar muita atenção. A música e os efeitos sonoros devem acompanhar os movimentos, as imagens, as transições e tudo mais. Os sons precisam fazer sentido com o que aparece na imagem. O vídeo deve ser atraente e dinâmico, com aparência bem profissional. Em no máximo 2 minutos, as pessoas precisam conhecer o potencial de tudo isso. Nos primeiros 3 segundos, o vídeo precisa chamar a atenção.
```

---

## 4 · Copiar o estilo de um vídeo de que você gostou

Se você vir no X ou no LinkedIn um vídeo feito com código e o autor compartilhar o prompt, não copie tudo. Peça para adaptar a **estrutura** ao seu produto.

```text
Vou enviar o prompt de um vídeo que vi e ficou espetacular. Adapte o que fizemos ao estilo desse prompt e crie algo parecido para [produto]. Primeiro, me entregue o prompt completo para eu colar em outra conversa:

[cole o prompt aqui]
```

Se ficar curto:

```text
Você pode fazer mais longo, se quiser. Faça o tempo que considerar necessário para mostrar tudo o que o produto faz.
```

---

## 5 · Reutilizar um prompt que já funcionou

```text
Vou enviar um prompt que me ajudou muito a fazer um vídeo explicativo sobre outro assunto. Quero usar a estrutura dele: aproveite somente a estrutura, não o conteúdo. Adapte todo o conteúdo para fazer um vídeo sobre [tema], com tudo o que conversamos. Primeiro, me devolva o prompt adaptado e explique tudo. Depois, em outra sessão, vou criar o vídeo com código.

[cole o prompt aqui]
```

Os modelos `02` a `04` desta pasta são justamente isso: estruturas testadas para você adaptar.

---

## 6 · Começar a produção com um prompt longo

```text
Crie este vídeo em [pasta do projeto]:

[cole o prompt de filme aqui]
```

A skill pedirá os materiais de entrada (logo, capturas de tela, música, clipe) e mostrará o mapa de pulsos e alguns quadros-chave antes de escrever o vídeo inteiro.

---

## 7 · Ajustar o gancho

O gancho é o que mais passa por ajustes. Peça algo concreto: o que precisa aparecer e por quê.

```text
É importante que o hook seja muito bom. Vamos falar de [ferramenta ou marca], então ela também precisa aparecer no começo, junto com [sua marca]. Encontre a melhor maneira de fazer isso para que o gancho visual seja muito, muito bom e prenda a atenção.
```

Quando estiver bom:

```text
O hook está aprovado: produza o filme vertical completo com esta abertura.
```

---

## 8 · Variações e autonomia

```text
Agora gere a versão horizontal 1920×1080 com o mesmo código e recomponha o enquadramento. Não estique nem recorte a versão vertical.
```

```text
Vá até o fim com o que você considerar melhor.
```

Use quando já tiver aprovado a direção e não quiser mais perguntas.

---

## Novas variações para testar

Estas não vêm de produções anteriores: são sugestões para começar outros tipos de vídeo cobertos pela skill.

**Explicar um repositório do GitHub**
```text
Leia o repositório [URL ou pasta] e use a skill criar-videos-con-codigo para fazer um vídeo de 60 segundos que explique o que ele faz e por que é útil para quem não programa. Mostre somente o que já está implementado, não o roadmap.
```

**Demo de um app com capturas reais**
```text
Na pasta [pasta], há capturas reais do [app]. Use criar-videos-con-codigo para fazer uma demo vertical de 45 segundos: problema, ação no app, resultado e chamada para ação. Anime as capturas com zoom e cursor. Não invente telas que não apareçam nas capturas.
```

**Dados que contam uma história**
```text
Com os dados de [fichero.csv], use criar-videos-con-codigo para fazer um vídeo de 30 segundos que conte uma única conclusão. Transforme as barras e os números uns nos outros, deixando as unidades sempre visíveis. Use música tranquila, sem efeitos em cada barra.
```

**Anúncio com sua própria voz**
```text
Tenho esta locução gravada: [audio.wav]. Use criar-videos-con-codigo para montar um anúncio vertical de motion graphics. Meça a voz antes de definir os tempos: cada ideia que eu disser precisa aparecer na tela no momento em que eu disser.
```
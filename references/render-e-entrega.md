# Renderização e entrega

## Projeto e contrato

Separar `docs`, `src`, `assets`, áudio, renderizações e revisões. Manter os recursos locais e materializar as fontes antes de capturar. Criar `window.videoSpec={width,height,fps,duration}`, `window.seek(t)` determinístico e `window.renderReady` como uma promessa que aguarde imagens, fontes e outros recursos. Cada instante deve poder ser avaliado após qualquer salto temporal.

Resolver as dependências reais antes de prometer uma exportação. HTML precisa de Node, Playwright, Chromium e FFmpeg. `bash scripts/preparar-entorno.sh --comprobar` informa o que está faltando; sem a opção, instala Playwright e Chromium em `~/.cache/crear-videos-con-codigo`, sem sudo. O renderizador resolve o Playwright a partir de uma instalação normal, `VIDEO_NODE_MODULES`, `CODEX_PRIMARY_RUNTIME_NODE_MODULES` ou dessa pasta, e aceita `VIDEO_CHROMIUM_PATH`. Não use uma sessão de navegador pessoal para renderizar. Execute `--help` antes do primeiro uso.

A verificação de determinismo tolera o ruído de antialiasing do texto no Chrome (diferença máxima de 32/255 em menos de 0,2% dos pixels). Se falhar, há um estado real que depende da ordem dos saltos: procure a causa, não aumente a tolerância.

Para começar pelo exemplo em Canvas, copie `assets/base-video/index.html` para o projeto e `assets/motion/motion.mjs` para junto desse HTML. O exemplo contém uma transformação, não um estilo final. Altere o design e o conteúdo conforme o brief.

## Exportações

Substitua os caminhos conforme o projeto e a localização real da skill:

```bash
node /ruta/skill/scripts/render-video.mjs --project /ruta/proyecto --output /ruta/proyecto/renders/prueba.mp4 --start 4 --end 9 --width 540 --height 960 --fps 30 --audio /ruta/proyecto/audio/mezcla.wav
node /ruta/skill/scripts/render-video.mjs --project /ruta/proyecto --output /ruta/proyecto/renders/final.mp4 --fps 60 --audio /ruta/proyecto/audio/mezcla.wav
node /ruta/skill/scripts/render-video.mjs --project /ruta/proyecto --output /ruta/proyecto/renders/portada.png --still 1.8
```

`--start`/`--end` selecionam um intervalo do relógio original e recortam o áudio a partir da mesma origem. `--duration` altera a duração declarada do projeto; não use essa opção no lugar de `--end` para inspecionar um trecho. A duração é arredondada para quadros completos. `--still` usa tempo absoluto. `--overwrite` permite substituir uma exportação explicitamente.

Para motion blur, adicione `--subframes 4 --shutter 0.5`. Cada quadro calcula a média de amostras ao redor do seu instante; `--subframes 1` é o valor padrão. Teste a nitidez e o custo antes da renderização completa. Não use supersampling para disfarçar um movimento ruim.

O motor HTML serve apenas os arquivos do projeto, bloqueia solicitações externas e verifica o seek após um salto para trás. Inclua os recursos remotos no projeto primeiro. H.264 e yuv420p exigem dimensões pares.

## Alternativa SVG

Crie um módulo próprio com `VIDEO_SPEC` e `frame(t,width,height)` que retorne o SVG completo. Python calcula o estado; CairoSVG não executa JS nem animações SVG. São necessários Python, CairoSVG, FFmpeg e Pillow para desfoque temporal. Consulte os limites de filtros, tipografia e recursos antes de aceitar esse caminho. Mantenha a direção aprovada; não substitua uma cena complexa por cartões estáticos sem avisar.

```bash
python3 /ruta/skill/scripts/render-svg.py --scene /ruta/proyecto/scene.py --output /ruta/proyecto/renders/prueba.mp4 --start 1 --end 5 --audio /ruta/proyecto/audio/mezcla.wav --subframes 4
python3 /ruta/skill/scripts/render-svg.py --scene /ruta/proyecto/scene.py --output /ruta/proyecto/renders/final.mp4
```

O SVG usa recursos embutidos e fontes instaladas; inclua ou documente as dependências. Teste os saltos temporais e as mudanças de formato. Não considere o HTML testado com base em testes de SVG.

## Referências e revisão

```bash
python3 /ruta/skill/scripts/extract-reference.py referencia.mp4 --output-dir refs/analisis --interval 0.5
python3 /ruta/skill/scripts/inspect-video.py renders/final.mp4 --output-dir reviews --beats beats.json --strip 4.2
```

As folhas são paginadas. Leia `reference.json` para saber se o limite máximo de amostras deixou a cobertura incompleta; continue pelos trechos necessários. O extrator não baixa arquivos nem comprova o acesso a uma URL. O inspetor não escuta nem reproduz o vídeo por conta própria.

## Entrega

Entregue o MP4 no formato aprovado e as fontes editáveis com os recursos permitidos, o mapa musical, o roteiro, o brief e os prompts usados, as instruções reais e a revisão. Crie uma capa intencional; não dependa do primeiro quadro se ele não representar a peça. Salve conforme o ambiente. Não inclua recursos ou dados de clientes nesta skill.
# Revisão com evidências

## Compare o teste com o briefing

Observe amostras no tamanho de celular e sequências consecutivas ao redor de ações difíceis. Reproduza e ouça quando possível. Não avance para a produção completa só porque uma nota foi atribuída automaticamente.

| Critério | Evidência | Problema que exige correção |
| --- | --- | --- |
| Gancho | Abertura e primeiro resultado visível | Início vazio ou tardio |
| Clareza | Ação e consequência reconhecíveis | Decoração que não explica |
| Continuidade | Sequência ao redor da mudança | Saltos ou perda de identidade |
| Variedade | Comparação de planos | Mesma composição repetida sem intenção |
| Leitura | Imagens a 360 px e tempo de exibição suficiente | Texto cortado, minúsculo ou rápido demais |
| Movimento | Reprodução e tiras de quadros | Aceleração abrupta ou falta de foco |
| Marca/conteúdo | Recursos e fontes conferidos | Interface inventada apresentada como real |
| Som | Escuta, marcações e nível | Descompasso, final truncado ou mixagem ruim |

Em movimento contínuo, uma sucessão de telas independentes falha, mesmo que o arquivo esteja correto. Em uma explicação sóbria, respeite as pausas úteis e não force efeitos.

## Registro

Registre o tempo, a observação, a consequência, a gravidade, a correção e o estado. Separe fatos de hipóteses. Priorize conteúdo falso, falta de legibilidade, descompasso e descontinuidade. Corrija até três problemas principais por rodada e verifique o que foi alterado. Após três rodadas sem resolver uma causa, mude a abordagem ou o recurso.

## Níveis separados

1. Arquivo: metadados, duração, quadros, áudio e decodificação.
2. Amostras: folhas paginadas, abertura, encerramento e momentos críticos.
3. Movimento: reprodução contínua com revisão de leitura e continuidade.
4. Escuta: música, voz, equilíbrio e sincronia percebida.

Registre como realizado, com falha ou pendente. Não marque movimento ou som como revisados por ter lido o código. Preencha os campos de `inspection.json` somente com ações realizadas. Se não houver reprodução ou escuta, apresente uma revisão pendente; não declare que o resultado criativo foi validado.

## Comandos

```bash
python3 scripts/inspect-video.py final.mp4 --output-dir reviews --samples 12
python3 scripts/inspect-video.py final.mp4 --output-dir reviews-beats --beats beats.json
python3 scripts/inspect-video.py fragmento.mp4 --output-dir reviews-tramo --beats beats.json --timeline-start 8 --strip 9.2
```

`--strip` adiciona doze quadros ao redor de um tempo do projeto; pode ser repetido. `--times 0,1.5,7.9` adiciona tempos específicos. O relatório lista todas as folhas. Extraí-las não comprova que foram observadas.
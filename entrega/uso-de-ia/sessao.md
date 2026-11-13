# Registro da sessão de uso de IA

## Sobre este arquivo

Este é um resumo em frases curtas das conversas com a IA durante o teste.


## Ferramenta

- Assistente: Claude (Anthropic).
- Modelo: 5.5 Sonnet

## Combinado de trabalho

- Ela formula a hipótese primeiro. A IA questiona.
- Ela escreve cada correção. A IA revisa o diff e aponta casos de borda.
- Ela escreve o rascunho do README-ENTREGA. A IA revisa.
- Cada defeito vira um commit próprio.
- Conceitos novos são explicados quando ela pede "me explica".
- O uso de IA é declarado.

**Ambiente**

- A IA explicou venv.
- Priscila instalou o Python 3.11.9, pois usava o 3.15 que está em fase de testes, criou a venv e rodou todos os comandos.
- Ela copiou o projeto para `C:\dev\onfly-desafio`, fora do OneDrive.

**Defeito 1: conversão de câmbio**

- O teste esperava 642.00 e recebeu 118.45.
- Priscila fez a conta: 118,45 − 100 = 18,45, e 100 ÷ 5,42 = 18,45.
- Ela concluiu que o código dividia pela taxa.
- A hipótese inicial era "o câmbio está desatualizado". Ela a descartou com a conta e com a regra do README de não alterar `data/`.
- Ela escreveu a correção: `return amount * rate`.


**Defeito 2: noites**

- O resultado de 30/01 a 02/02 era −28. O esperado era 3.
- Priscila notou que 2 − 30 = −28.
- Ela concluiu que o código usava o dia do mês.
- Ela escreveu a correção: `(checkout - checkin).days * rooms`.


**Defeito 3: status faturável**

- O total era 120.00. O esperado era 100.00.
- Priscila notou que 100 + 20 = 120. O NO_SHOW tinha passado pelo filtro.
- Ela concluiu que `status != "CANCELLED"` é uma lista de exclusão.
- Ela escreveu a correção: `status == "CONFIRMED"`.

**Defeito 4: ranking de hotéis**

- O resultado era `['H04','H03','H02']`. O esperado era `['H01','H02','H03']`.
- Priscila concluiu que o valor estava em ordem crescente.
- Ela considerou `reverse=True` e viu que inverteria o desempate.
- A IA sugeriu as opções de ordenação. Ela escolheu o sinal de menos.
- Ela escreveu a correção: `key=lambda item: (-item[1]["amount"], item[0])`.
- O diff teve duas rodadas de limpeza de espaços em branco. O resultado final ficou limpo.

**Defeito 5: limite de 200 linhas**

- Priscila achou o defeito lendo o código com o README ao lado.
- A pista foi `total_reservations: 200`, um número redondo.
- Ela procurou o trecho suspeito.
- Ela removeu as duas linhas do `if len(rows) == 200: break`.
- Nenhum teste detectava esse defeito.

**Commit do defeito 5**

- Priscila mostrou o `git diff`. A IA confirmou que o diff estava limpo.
- Ela fez o commit `711d41c`.
- O log passou a ter sete commits.

**Conferência dos números**

- Ela rodou o CLI. A saída foi 300 reservas, 235 confirmadas, 1347 noites e R$ 396170.00.
- Ela colou o `report.json`.
- A IA somou o `by_month`. Reservas e noites bateram.
- O `total_brl` dos meses somou 396170.01, contra 396170.00 do resumo.
- Priscila trouxe o README do teste.
- A regra "arredondar só na serialização" explicou a diferença de um centavo.

**Revisão do `.gitignore`**

- Priscila leu o conteúdo e conferiu.
- A IA também revisou e viu que continha `.venv/`, `__pycache__/` e `.pytest_cache/`.

**Decisão sobre o `tools/conferir.py`**

- A IA perguntou se o script deveria importar algo de `src/onfly_report`.
- Priscila respondeu que não, para não trazer um defeito do CLI para a conferência.
- A IA concordou. A decisão ficou registrada.
- O script ficou em `tools/`, na raiz do projeto.

**Escrita do `tools/conferir.py`**

- Priscila escreveu o script em etapas pequenas, rodando a cada uma.
- A IA explicou `csv.DictReader`.
- Etapa 1: leitura das taxas em um dicionário com `Decimal`.
- Etapa 2: leitura das reservas e filtro por `CONFIRMED`.
- Etapa 3: conversão para reais.
- Etapa 4: soma do total e arredondamento só no final.
- Etapa 5: cálculo das noites.
- Priscila corrigiu sozinha vários erros de nome apontados pelo Python, como `KeyError` e `NameError`.
- Ela decidiu mover o `quantize` para depois do laço.
- Ela fez a conta de uma reserva em euros à mão. O código confirmou o resultado.
- Resultado final do script: `235 396170.00 1347`.
- Priscila fez o commit `bd88d78`. O log passou a ter oito commits.

**README-ENTREGA**

- Priscila escreveu a investigação dos cinco defeitos com as próprias palavras.
- A IA revisou o conteúdo e apontou ajustes: dois deslizes de número e de nome de coluna, e sobras de modelo.
- Priscila corrigiu os deslizes de número e de nome de coluna.
- A IA formatou o texto dela em Markdown.

## O que a IA escreveu pronto

- A formatação do `README-ENTREGA.md` e o molde da `declaracao.md`.
- Exemplos de brinquedo, com outros assuntos, de `csv.DictReader`, de dicionário e de `quantize`.
- Este resumo.

## O que Priscila fez

- Configurou o ambiente e rodou todos os comandos.
- Formulou as hipóteses dos defeitos 1 a 5.
- Localizou os trechos no código.
- Escreveu as correções dos cinco defeitos.
- Escolheu o sinal de menos no ranking.
- Revisou os diffs e fez os commits.
- Decidiu que o `conferir.py` não importa código do CLI.
- Escreveu o `tools/conferir.py`.
- Escreveu o texto da investigação no README-ENTREGA.

## Resultados verificados

- `pytest -q`: 5 passed.
- Amostra `exemplo-validacao.csv`: bateu com a tabela do README.
- CLI no arquivo real: 300 reservas, 235 confirmadas, 1347 noites, R$ 396170.00.
- `tools/conferir.py`: 235, 396170.00 e 1347, sem usar código do CLI.

## Logs da interação com a IA

No arquivo "transcricao.md".
# Declaração de uso de IA

## Ferramenta e modelo

- Ferramenta: Claude (Anthropic), no claude.ai.
- Modelo da conversa de 12/11/2026: Claude Sonnet 5.5.
- As sessões estão em `entrega/uso-de-ia/`.

## Como trabalhei

Usei a IA como copiloto de estudo e revisão: eu formulava e escrevia, ela questionava e revisava.

- Li os arquivos do projeto para compreensão da arquitetura aplicada no projeto.
- Eu formulava a hipótese primeiro.
- A IA fazia perguntas e não entregava a solução pronta.
- Eu escrevia cada correção.
- A IA revisava o diff e apontava casos de borda.
- Cada defeito virou um commit próprio.

## O que a IA fez

- Explicou conceitos: venv, `csv.DictReader` e `quantize`.
- Guiou o método de investigação com perguntas.
- Revisou os diffs antes dos commits.
- Sugeriu cenários de teste.
- Explicou a diferença de um centavo à luz do README do teste.
- Revisou meu `README-ENTREGA.md` e apontou ajustes.
- Formatou meu texto do `README-ENTREGA.md` em Markdown e acrescentou as seções de validação, conferência independente, arquivos revisados e uso de IA.
- Montou o molde desta declaração.

## Código que a IA escreveu pronto

- Exemplos de brinquedo, com outros assuntos, de `csv.DictReader`, de dicionário e de `quantize`.
- O resumo `sessao.md`, o molde desta declaração e a formatação do `README-ENTREGA.md`.


## O que eu fiz

- Configurei o ambiente: Python 3.11.9, venv, dependências, PowerShell e VS Code.
- Rodei todos os comandos.
- Formulei as hipóteses dos defeitos 1 a 5. Exemplos: `118,45 − 100 = 18,45` e `100 ÷ 5,42 = 18,45`; `2 − 30 = −28`; "o NO_SHOW entrou e o CANCELLED ficou de fora".
- Localizei os trechos no código.
- Escrevi as correções dos cinco defeitos.
- Encontrei o defeito 5 lendo o código com o README ao lado. 
- Escolhi o sinal de menos no ranking.
- Revisei os diffs e fiz os commits.
- Decidi que o `tools/conferir.py` não importa nada de `src/onfly_report`, para a conferência ser independente do código do CLI.
- Escrevi o `tools/conferir.py` em etapas e conferi cada uma rodando.
- Escrevi o texto da investigação do `README-ENTREGA.md`.

## Tropeços e correções

Registro estes pontos porque fazem parte do processo.

- **Defeito 4:** o diff teve espaços em branco a mais. Fiz duas rodadas de limpeza até ficar limpo.
- **Defeito 5:** rodei `git add` sem o caminho do arquivo. O git não adicionou nada. Repeti o comando com o caminho.
- **`tools/conferir.py`:** errei nomes de colunas e de variáveis algumas vezes (`KeyError`, `NameError`). Corrigi lendo a mensagem de erro do Python.
- **Conta à mão:** a conversão de uma reserva em euros, feita de cabeça, saiu com diferença de centavos. O código chegou ao valor exato.

## Resultado

- `pytest -q`: 5 passed.
- CLI no arquivo real: 300 reservas, 235 confirmadas, 1347 noites, R$ 396170.00.
- `tools/conferir.py`: 235, 396170.00 e 1347, calculados sem usar código do CLI.



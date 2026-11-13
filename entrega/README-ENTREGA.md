# Teste Onfly - Sistema de Reserva Para Hotéis

O objetivo do teste é encontrar e consertar linhas de código do CLI do projeto para que ele gere relatórios do tipo JSON com dados confiáveis. Encontrei e corrigi cinco defeitos. Foi feita também a leitura e verificação minuciosa dos arquivos e módulos não afetados.

## 💻 Ambiente

* **SO e Ferramentas:** Windows, PowerShell, VS Code.
* **Python:** Instalei o Python 3.11.9 via winget (antes possuía apenas a versão 3.15 alpha).
* **Diretório:** Projeto copiado do Drive para `C:\dev\onfly-desafio`.
* **Ambiente Virtual:** venv criado em `.venv`, ativado com `.venv\Scripts\Activate.ps1`. Dependências do `requirements-dev.txt` (pytest, ruff, etc.) instaladas.

## 🐛 Defeitos Encontrados e Corrigidos

### Defeito 1 – Conversão de câmbio (`services/currency_converter.py`)

* **Sintoma:** O teste esperava o resultado de `642.00` (100 BRL + 100 USD a 5,42), mas recebeu `118.45`.
* **Raciocínio:** `118,45 − 100 = 18,45`, e `100 ÷ 5,42 = 18,45`, ou seja, o programa estava codado para dividir pela taxa. Primeiro, pensei em qual conta possível eu receberia o resultado de 118.45, foi aí que a divisão foi encontrada. O cálculo correto para achar o valor total é multiplicar os valores.
* **Causa raiz:** A função `Decimal(str(float(amount) / float(rate)))` dividia em vez de multiplicar e passava por `float`, o que contradiz a regra de usar `Decimal` descrita no README.
* **Correção:** Troquei a lógica para a multiplicação com `return amount * rate` e limpei as conversões desnecessárias.
* **Por quê:** Usar `Decimal(str(float(...)))` não conserta nada, pois a imprecisão entra no float antes.

### Defeito 2 – Noites (`services/stay_calculator.py`)

* **Sintoma:** As datas de `30/01` até `02/02` devolviam `-28`, quando o correto é `3`.
* **Raciocínio:** `2 − 30 = −28`. O código subtraía apenas o dia do mês e ignorava a virada de mês/ano.
* **Causa raiz:** O trecho `(checkout.day - checkin.day) * rooms` usava o atributo `.day` (dia do mês) em vez de subtrair datas completas.
* **Correção:** Alterei para `return (checkout - checkin).days * rooms`.

### Defeito 3 – Status faturável (`services/status_policy.py`)

* **Sintoma:** O total faturado resultou em `120.00`, mas o esperado era `100.00`. Dados enviados: CONFIRMED (100), CANCELLED (50) e NO_SHOW (20).
* **Raciocínio:** `100 + 20 = 120`, então o NO_SHOW passou indevidamente pelo filtro.
* **Causa raiz:** O código utilizava `return status != "CANCELLED"`, o que deixava passar o NO_SHOW (e qualquer outro status não previsto).
* **Correção:** Troquei para `return status == "CONFIRMED"` (transformando em uma lista de inclusão rigorosa, como manda a regra).
* **Verificado:** A ordem de processamento ("contar status → filtrar CONFIRMED → agregar") já estava correta em `report_builder.py`.

### Defeito 4 – Ranking de hotéis (`services/report_builder.py`)

* **Sintoma:** O resultado retornava `['H04','H03','H02']` em vez de `['H01','H02','H03']`.
* **Raciocínio:** O `key=(valor, hotel_id)` ordenava o valor de forma crescente. Pensei na utilização de `reverse=True`, o que estragaria o desempate (hotel_id crescente, que já estava correto), pois inverteria os dois critérios.
* **Causa raiz:** Valor ordenado de forma crescente, quando o README pede decrescente, mantendo o desempate por hotel_id de forma crescente.
* **Correção:** Alterei para `key=lambda item: (-item[1]["amount"], item[0])` e adicionei um comentário curto explicando o sinal de menos. Escolhi essa abordagem em vez de fazer ordenação em duas passadas.

### Defeito 5 – Limite de 200 linhas (`repositories/csv_reservation_repository.py`)

* **Como foi achado:** Pela leitura atenta do código lado a lado com as regras de negócio, e não por falha no `pytest`. A pista foi `total_reservations: 200`, um número redondo e suspeito.
* **Causa raiz:** A instrução `if len(rows) == 200: break` dentro do laço de leitura cortava o arquivo arbitrariamente na 200ª reserva, de forma silenciosa.
* **Correção:** Removi as duas linhas responsáveis pelo limite.

**Impacto real no arquivo `reservas_hoteis.csv` (comprovado com a leitura de 300 reservas):**

| Campo | Antes (cortado em 200) | Depois (arquivo inteiro) | 
| ----- | ----- | ----- | 
| `total_reservations` | 200 | 300 | 
| `confirmed_reservations` | 153 | 235 | 
| `total_room_nights` | 909 | 1347 | 
| `total_amount_brl` | 249543.79 | 396170.00 | 

## 📖 Leitura e Revisão Integral do Código

Além de corrigir os pontos apontados pelo `pytest`, fiz questão de ler **todos** os arquivos do projeto (incluindo `cli.py`, `csv_rate_repository.py` e `row_parser.py`) com as regras de negócio lado a lado. O objetivo foi garantir que o contrato estava sendo cumprido na íntegra e procurar defeitos invisíveis aos testes. 

Durante essa varredura completa, atestei que:
- Os arquivos estão sendo abertos corretamente em `UTF-8` (respeitando nomes com acentos).
- O parâmetro `--top` e os códigos de saída do CLI (`0`, `1` e `2`) cumprem o contrato.
- A regra de ouro ("nunca use float no dinheiro") não estava sendo violada em nenhum outro ponto da aplicação além do defeito 1.

## 🧪 Validação e Conferência Independente

Para garantir a confiabilidade do CLI e validar a solução do defeito 5, criei um script de validação independente em `tools/conferir.py`.

* **Independência:** O script foi escrito do zero utilizando `csv.DictReader` e não importa nenhum módulo ou função da pasta `src/onfly_report`. Isso garante que a validação não herde os possíveis vícios ou falhas da implementação principal.
* **O "centavo" de diferença no by_month:** Durante a validação, a soma mês a mês dos valores do arquivo real resultou em `396170.01`, enquanto o resumo global do CLI apontou `396170.00`. Isso ocorreu porque o CLI segue estritamente a regra de negócio do projeto: *"Some os valores exatos e arredonde só na serialização"*. O somatório isolado dos valores já arredondados mês a mês gera pequenas distorções frente ao montante geral exato. Isso atesta que a regra de aplicar `ROUND_HALF_UP` apenas no final está fielmente implementada.

**Resultado da Suíte de Testes:**

* Comando: `pytest -q`
* Resultado: **5 passed** (todos os testes originais mantidos intactos e passando).

## 📦 Arquivos Entregues

A estrutura final da entrega contempla:

1. Código-fonte corrigido.
2. `tools/conferir.py` (Script de dupla checagem independente).
3. Este `README-ENTREGA.md` com a documentação investigativa.
4. Diretório `entrega/uso-de-ia/` contendo a `declaracao.md` e os logs detalhados das sessões (`sessao.md`, `sessao-01.md`, `sessao-02.md`).
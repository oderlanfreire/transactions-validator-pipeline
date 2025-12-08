# Payment Authorization Transactions Validator

Pipeline local em Python para **validação e padronização de eventos de autorização de pagamentos** (cartão, PIX e boleto), com foco em qualidade de dados, rastreabilidade e boas práticas de engenharia para portfólio.

Este projeto simula um cenário comum em times de Dados/Fintech/E-commerce:  
**ingestão de arquivos transacionais → normalização → validação de regras → separação de válidos/inválidos → geração de arquivo de erros**.

---

## Objetivos

- Criar uma pipeline simples e confiável para validação de arquivos de autorizações.
- Separar registros **válidos** e **inválidos** com base em regras do domínio.
- Gerar arquivo de erro `.err` no padrão: `transaction_id|erro`.
- Garantir rastreabilidade via logs com `trace_id`.
- Demonstrar boas práticas de engenharia de dados:
  - modularização
  - schema versionado
  - tratamento de tipos
  - testes unitários essenciais

---

## Escopo

### Incluído

- Normalização de headers.
- Renomeação de colunas via aliases.
- Conversão de tipos via `dtype_mappings`.
- Validações macro do domínio de autorizações.
- Geração de:
  - `output/valid/*.csv`
  - `output/invalid/*.csv`
  - `output/errors/*.err`
- Movimentação do arquivo processado para `hist/`.

### Fora do escopo

- Modelagem analítica completa (DW/BI).
- Detecção de fraude avançada.
- Streaming/real-time.
- Integrações com data lake/cloud.
---

## Estrutura do Projeto

```text
.
├── input/
├── output/
│   ├── valid/
│   ├── invalid/
│   └── errors/
├── hist/
├── logs/
│   └── pipeline/
├── schemas/
│   └── transactions_schema.json
├── modules/
│   ├── reader.py
│   ├── treatment.py
│   ├── validator.py
│   ├── writer.py
│   └── util.py
├── config/
│   └── setup_logging.py
├── tests/
└── transactions_pipeline_main.py
``` 

## Dataset

O schema principal prevê os campos:

### Required
- `transaction_id`
- `event_timestamp`
- `amount`
- `currency`
- `authorization_status`
- `payment_method`
- `payment_channel`
- `response_code`

### Optional
- `order_id`
- `merchant_id`
- `acquirer`
- `brand`
- `issuer`
- `payer_bank`
- `decline_reason_category`
- `card_type`

---

## Regras de Negócio Implementadas

As validações atuais são **macro-regras** típicas de um pipeline de qualidade para autorizações:

1. **Campos obrigatórios não podem ser nulos**
   - Qualquer linha com `required_columns` ausente/nulo é inválida.

2. **Amount não pode ser negativo**
   - `amount < 0` → inválido.

3. **APPROVED deve ter response_code = "00"**
   - `authorization_status == APPROVED` e `response_code != "00"` → inválido.

4. **DECLINED não pode ter "00"**
   - `authorization_status == DECLINED` e:
     - `response_code == "00"` **ou**
     - `response_code` fora do conjunto esperado (`05, 51, 54, 91`)
     → inválido.

5. **PIX/BOLETO não devem carregar campos de cartão**
   - Se `payment_method in {PIX, BOLETO}` e algum de:
     - `brand`, `acquirer`, `issuer`
     estiver preenchido → inválido.

Cada linha inválida recebe `error_reason` no `invalid_df`.

---

## Como funciona o fluxo

1. `find_valid_file()` localiza arquivo em `input/`.
2. `smart_file_stem()` gera basename seguro para logs/outputs.
3. `setup_logging()` configura logs.
4. `read_file()` lê CSV/TXT.
5. Treatment:
   - `normalize()` headers
   - `rename_columns()` com aliases (suporta aliases aninhados)
   - `convert_data_types()` com `dtype_mappings`
6. `validate()` aplica regras e gera:
   - `valid_df`
   - `invalid_df` com `error_reason`
7. `save_data()`:
   - salva valid/invalid
   - gera `.err` com `transaction_id|error_reason`
   - move arquivo original para `hist/`

---

## Configuração do Schema

A pipeline é guiada por:

`schemas/transactions_schema.json`

Ele contém:

- `required_columns`
- `optional_columns`
- `dtype_mappings`
- `column_aliases` (hierárquico por grupos)

Isso permite:
- suportar variações de header sem alterar código
- evoluir regras com versionamento claro de schema

---

## Como executar

### 1) Instale dependências
```bash
pip install -r requirements.txt
```
### 2) Coloque um arquivo em input/

Extensões aceitas:

- `.csv`
- `.txt`
- `.csv.gz`
- `.txt.gz`

### 3) Rode a pipeline
```bash
sh run_pipeline.sh
```
ou diretamente
```bash
python transactions_pipeline_main.py
```

## Saídas

Após execução:

### Válidos

- `output/valid/{basename}_valid_{timestamp}.csv`

### Inválidos

- `output/invalid/{basename}_invalid_{timestamp}.csv`

### Erros

- `output/errors/{basename}_{timestamp}.err`

### Formato sem header
```bash
tx123|amount inválido
tx456|campos obrigatorios faltantes
```

### Histórico

- arquivo original movido para:
    - `hist/{timestamp}_{filename_original}`

## Logs

Os logs são gerados em:
- `logs/pipeline/{basename}_{TRACE_ID}.log`

Formato:
```bash
timestamp - trace_id - logger - level - message
```
---

## Testes

Execute:

```bash
pytest -q
```


Cobertura sugerida:
- `reader`
    - leitura ok
    - arquivo inexistente

- `treatment`
    - normalize
    - rename nested
    - convert datetime

- `validator`
    - 1 teste por regra macro

- `writer`
    - geração de valid/invalid/.err
    - move para hist
---

## Decisões de Design

### Schema-driven pipeline
    Regras e tipos saem do JSON para facilitar evolução e manutenção.

### Error Reason no validator
    O writer apenas serializa transaction_id|error_reason, mantendo o domínio no módulo correto.

### Separação de responsabilidades
- `reader → I/O de leitura`
- `treatment → padronização e tipos`
- `validator → regras de domínio`
- `writer → persistência`
- `util → funções de suporte`
---

## Requisitos
- Python 3.10+
- Dependências em `requirements.txt`

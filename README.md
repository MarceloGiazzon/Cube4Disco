# Cube4Disco

Conector analítico multidimensional (OLAP) e motor de inferência causal para o agronegócio. Integra dados transacionais de ERPs com dados públicos exógenos, como clima, cotações e indicadores macroeconômicos, para revelar relações de causa e efeito sem comprometer a privacidade dos dados.

## 1. Visão Geral

ERPs e sistemas transacionais analisam as operações da porteira para dentro. Quando ocorrem oscilações de faturamento, atrasos na aplicação de insumos ou quebras de safra, os relatórios tradicionais registram o impacto financeiro, mas muitas vezes não identificam as causas externas.

O Cube4Disco conecta dados operacionais e variáveis externas para apoiar análises agrícolas. O sistema:

- Conecta-se a bancos e ERPs agrícolas, como Totvs Protheus, Siagri e bases SQL legadas.
- Mapeia schemas relacionais para entidades canônicas com apoio de inferência semântica.
- Anonimiza e agrega registros na infraestrutura de origem, com foco na proteção de dados (LGPD/GDPR).
- Cruza transações internas com séries temporais públicas de fontes como INMET, CEPEA/Esalq, BACEN e CONAB.
- Aplica testes econométricos, incluindo causalidade de Granger, para investigar relações temporais e gerar diagnósticos.

## 2. Arquitetura

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        INFRAESTRUTURA LOCAL (ON-PREMISES)              │
│                                                                        │
│   ┌─────────────────────┐               ┌──────────────────────────┐   │
│   │   ERP / Banco Agro  │               │    Cube4Disco Agent      │   │
│   │ (Protheus, Siagri,  │ ── Local ───> │  - Inspeciona DDL/Schema │   │
│   │  SQL Server, SQLite)│    Query      │  - Agrega & Anonimiza    │   │
│   └─────────────────────┘               └─────────────┬────────────┘   │
└───────────────────────────────────────────────────────┼────────────────┘
                                                        │ HTTPS Outbound (TLS)
┌───────────────────────────────────────────────────────┼────────────────┐
│                   CUBE4DISCO CLOUD CORE / API SERVICE │                │
│                                                       ▼                │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                  FastAPI Gateway / Endpoints                   │   │
│   │             (Autenticação, Gestão de Jobs & Fila)              │   │
│   └───────────────────────────────┬────────────────────────────────┘   │
│                                   │                                    │
│   ┌───────────────────────────────▼────────────────────────────────┐   │
│   │                     Workers Celery / Redis                     │   │
│   │                                                                │   │
│   │  ┌─────────────────────────┐      ┌─────────────────────────┐  │   │
│   │  │   DuckDB In-Memory OLAP │ <──> │ Conectores Públicos     │  │   │
│   │  │  (Construção de Cubo)   │      │ (INMET, CEPEA, BACEN)   │  │   │
│   │  └────────────┬────────────┘      └─────────────────────────┘  │   │
│   │               │                                                │   │
│   │  ┌────────────▼────────────┐      ┌─────────────────────────┐  │   │
│   │  │ Motor Estatístico Causal│ <──> │ Camada de Raciocínio IA │  │   │
│   │  │(Granger, Cointegração)  │      │(LLM: Validação/Insights)│  │   │
│   │  └─────────────────────────┘      └─────────────────────────┘  │   │
│   └────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

## 3. Principais Componentes

### 3.1. Cube4Disco Agent (On-Premises)

- **Extração segura:** coleta metadados e DDL do catálogo do banco local (`information_schema` e tabelas de sistema). Registros confidenciais de clientes, fazendas e faturamento nominal não devem sair da rede local sem anonimização.
- **Anonimização e agregação:** compacta transações em dimensões espaço-temporais, como `total_faturado` e `volume_sacas` agrupados por `codigo_ibge`, `semana_safra` e `codigo_ncm`.
- **Conectividade:** opera por requisições de saída via HTTPS (porta 443), sem exigir portas abertas ou IPs públicos na fazenda ou cooperativa.

### 3.2. Camada Semântica e De-Para Assistido

- **Schema matching com IA:** LLMs analisam dicionários de dados, como `SD2010`, `D2_QUANT` e `D2_TOTAL` do Protheus, e sugerem arquivos declarativos `mapping.yaml` para entidades canônicas.
- **Compilação determinística:** após a aprovação do mapeamento (human-in-the-loop), o sistema compila queries SQL nativas, sem depender continuamente de tokens de IA nas rotinas diárias.

### 3.3. Motor OLAP e Fontes Públicas

- **Cubo multidimensional (DuckDB + Polars):** processamento colunar em memória e integração com arquivos Parquet.
- **Meteorologia:** precipitação acumulada, anomalias de temperatura e umidade do solo (INMET, NOAA e Copernicus).
- **Mercado:** indicadores diários de preço à vista para soja, milho e café (CEPEA/Esalq, B3 e CBOT).
- **Macroeconomia:** câmbio PTAX e taxa Selic (Banco Central do Brasil).

### 3.4. Motor de Inferência Causal

Aplica testes de estacionariedade (ADF), cointegração e causalidade de Granger para avaliar se variações climáticas ou de mercado antecedem mudanças no comportamento de compra e entrega, reduzindo o risco de interpretar correlações espúrias.

## 4. Tech Stack

| Camada | Tecnologia | Papel |
| --- | --- | --- |
| Backend / API | Python 3.11+, FastAPI, Pydantic v2 | Gateway REST assíncrono e validação de contratos. |
| Motor analítico | DuckDB, Polars | Processamento colunar e operações OLAP em memória. |
| Fila assíncrona | Redis, Celery | Orquestração de pipelines analíticos desacoplados. |
| Econometria / Estatística | Statsmodels, NumPy, Pandas | Testes de hipótese temporal, cointegração e Granger. |
| Inteligência artificial | OpenAI API / modelos locais via Ollama | Pareamento semântico de schemas e síntese de diagnósticos. |
| Agente local | Python nativo, SQLite / drivers relacionais | Leitura de metadados e agregação segura. |

## 5. Estrutura do Repositório

```text
Cube4Disco/
├── agent/                  # Componente On-Premises do cliente
│   ├── extractor.py        # Inspeciona DDL e tabelas de catálogo
│   ├── anonymizer.py       # Agrupa métricas e remove PII via Polars
│   └── client.py           # Cliente HTTP de saída (porta 443)
├── api/                    # Web Service FastAPI
│   ├── routes/             # Endpoints de controle e submissão de jobs
│   ├── schemas/            # Modelos de validação Pydantic
│   └── main.py             # Aplicação ASGI principal
├── config/                 # Gestão de variáveis de ambiente
│   └── settings.py
├── core/                   # Núcleo analítico da plataforma
│   ├── external/           # Conectores públicos (INMET, CEPEA, BACEN)
│   ├── olap/               # Motor DuckDB e montagem de cubos
│   ├── semantic/           # Schema matcher (LLM) e compilador SQL
│   └── stats/              # Motores de inferência causal e relatórios
├── data/mock/              # Bancos locais sintéticos para testes
├── scripts/                # Geradores de bases falsas e pipeline E2E
├── tests/                  # Suíte de testes unitários e de integração
├── workers/                # Tarefas em segundo plano (Celery)
├── docker-compose.yml      # Subida de Redis, API e Workers
└── requirements.txt        # Dependências do projeto
```

## 6. Guia de Início Rápido

### Pré-requisitos

- Python 3.11+
- Redis (local ou via Docker)
- Git

### Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/Cube4Disco.git
cd Cube4Disco

# 2. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
```

### Gerar dados sintéticos e executar a demonstração E2E

O projeto inclui um gerador de bases simuladas (banco ERP legado e balança de armazém) e um pipeline de demonstração.

```bash
# Gerar bases SQLite em data/mock/
python3 scripts/seed_fake_dbs.py

# Executar a demonstração ponta a ponta
python3 scripts/run_pipeline_demo.py
```

### Executar via Docker Compose

Para subir a API, os workers e o Redis:

```bash
docker-compose up --build
```

A documentação interativa da API estará disponível em <http://localhost:8000/docs>.

## 7. Uso da API

### Submeter análise de correlação

```bash
curl -X POST "http://localhost:8000/api/v1/correlate" \
  -H "Content-Type: application/json" \
  -d @- <<JSON
{
  "client_id": "coop_cerrado_01",
  "metric_target": "faturamento_fertilizantes_semanal",
  "geo_scope": {
    "level": "municipio",
    "ibge_codes": ["5107925", "5107909"]
  },
  "date_range": {
    "start": "2023-01-01",
    "end": "2024-12-31"
  },
  "external_dimensions": ["climate_inmet", "commodity_cepea"]
}
JSON
```

### Resposta imediata (202 Accepted)

```json
{
  "job_id": "c4d_8a92b1c4",
  "status": "PROCESSING",
  "estimated_time_seconds": 30,
  "check_status_url": "/api/v1/jobs/c4d_8a92b1c4"
}
```

### Consultar diagnóstico do job

```bash
curl "http://localhost:8000/api/v1/jobs/c4d_8a92b1c4"
```

### Resposta de sucesso (200 OK)

```json
{
  "job_id": "c4d_8a92b1c4",
  "status": "COMPLETED",
  "findings": [
    {
      "factor": "precipitacao_acumulada_defasada_21dias",
      "p_value": 0.003,
      "granger_causality": true,
      "relationship": "Atrasos em chuvas superiores a 20 dias reduzem as retiradas imediatas de fertilizantes em 28%.",
      "suggested_action": "Flexibilizar janelas de frete e prazos para adubos de cobertura."
    }
  ]
}
```

## 8. Roadmap

- [x] Especificação técnica e modelo conceitual da arquitetura.
- [x] Protótipo do agente local de inspeção de metadados e anonimização com Polars.
- [x] Motor de cubos analíticos com DuckDB e testes de causalidade de Granger.
- [x] API assíncrona FastAPI com filas em Celery/Redis.
- [x] Geradores de dados mock e pipeline de demonstração ponta a ponta.
- [ ] Conectores de produção automatizados para APIs REST do INMET e CEPEA.
- [ ] Integração com LLMs via LangChain/LiteLLM para geração de arquivos `mapping.yaml`.
- [ ] Interface visual para validação assistida de schemas (human-in-the-loop).

## 9. Licença

Este projeto é distribuído sob os termos da licença MIT. Consulte o arquivo `LICENSE` para obter mais detalhes.

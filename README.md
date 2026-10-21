# Cube4Disco

Conector analítico multidimensional (OLAP) e motor de inferência causal para o Agronegócio. Integra dados transacionais de ERPs locais com repositórios públicos (INMET, CEPEA, BACEN) para descoberta automatizada de correlações e relações de causa-efeito via IA e testes econométricos.

## Estrutura do Projeto
- `agent/`: Coletor local para extração de metadados, agregação e envio seguro (Outbound HTTPS).
- `api/`: Web service assíncrono em FastAPI para orquestração de análises e consulta de jobs.
- `core/olap/`: Motor colunar em DuckDB para junção de séries temporais e dimensões espaciais.
- `core/semantic/`: Mapeador de tabelas com IA (Schema Matching) e compilador SQL.
- `core/stats/`: Testes estatísticos de causalidade de Granger, cointegração e relatórios causais.
- `workers/`: Fila Celery / Redis para tarefas analíticas pesadas em background.

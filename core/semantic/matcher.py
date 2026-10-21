import json
from typing import Any, Dict

class SchemaSemanticMatcher:
    """
    Gera sugestões de De-Para entre esquemas de banco legado e o modelo canônico.
    """
    def generate_mapping_prompt(self, table_schema: Dict[str, Any]) -> str:
        return f"""
Atue como engenheiro de dados especialista em agronegócio e ERPs (ex: Totvs, Siagri).
Mapeie a tabela de origem para o modelo canônico do Cube4Disco:
Tabela Origem: {table_schema.get('table_name')}
Colunas: {json.dumps(table_schema.get('columns'))}

Retorne exclusivamente um JSON com as correspondências canônicas:
- data_transacao (DATE)
- valor_faturado (DECIMAL)
- volume_comercializado (DECIMAL)
- codigo_municipio_ibge (VARCHAR)
- codigo_produto (VARCHAR)
"""

from typing import Any, Dict

class SQLQueryCompiler:
    """
    Compila queries SQL determinísticas a partir de um mapeamento YAML/JSON aprovado.
    """
    @staticmethod
    def compile_extraction_query(mapping: Dict[str, Any]) -> str:
        fields = []
        for canonical, original in mapping["atributos"].items():
            fields.append(f"{original} AS {canonical}")
        
        select_clause = ", ".join(fields)
        table_name = mapping["tabela_origem"]
        return f"SELECT {select_clause} FROM {table_name}"

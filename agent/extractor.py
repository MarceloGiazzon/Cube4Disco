import sqlite3
from typing import Any, Dict, List

class LocalMetadataExtractor:
    """
    Inspeciona catálogos e esquemas do banco local sem ler registros sensíveis.
    """
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def extract_schema_ddl(self) -> List[Dict[str, Any]]:
        # Exemplo com SQLite local; para produção usar drivers Protheus/Oracle/SQLServer
        conn = sqlite3.connect(self.connection_string)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_summary = []
        for (table_name,) in tables:
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema_summary.append({
                "table_name": table_name,
                "columns": [{"id": col[0], "name": col[1], "type": col[2]} for col in columns]
            })
        conn.close()
        return schema_summary

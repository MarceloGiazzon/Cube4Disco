import duckdb
import polars as pl

class DataCubeEngine:
    """
    Gerencia o cubo de dados analítico multidimensional em DuckDB.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.conn = duckdb.connect(db_path)

    def register_client_data(self, df: pl.DataFrame, table_name: str = "fato_erp"):
        self.conn.register(table_name, df.to_arrow())

    def build_multidimensional_cube(self) -> pl.DataFrame:
        query = """
        SELECT 
            c.codigo_ibge,
            c.data,
            c.total_faturado,
            w.precipitacao_mm,
            p.preco_medio_saca
        FROM fato_erp c
        LEFT JOIN dim_clima w 
            ON c.codigo_ibge = w.codigo_ibge AND c.data = w.data
        LEFT JOIN dim_mercado p 
            ON c.data = p.data
        """
        arrow_result = self.conn.execute(query).arrow()
        return pl.from_arrow(arrow_result)

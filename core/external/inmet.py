from typing import Any, Dict, List
import polars as pl

class INMETConnector:
    """
    Coletor de dados meteorológicos históricos e previsões.
    """
    def fetch_historical_precipitation(self, ibge_code: str, start_date: str, end_date: str) -> pl.DataFrame:
        # Mock de ingestão estruturada
        return pl.DataFrame({
            "codigo_ibge": [ibge_code],
            "data": [start_date],
            "precipitacao_mm": [25.4],
            "temp_max": [31.2]
        })

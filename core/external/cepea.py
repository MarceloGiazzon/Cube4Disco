import polars as pl

class CEPEAConnector:
    """
    Coletor de cotações agropecuárias (CEPEA/ESALQ, B3, Chicago).
    """
    def fetch_commodity_price_series(self, commodity: str, start_date: str, end_date: str) -> pl.DataFrame:
        return pl.DataFrame({
            "commodity": [commodity],
            "data": [start_date],
            "preco_medio_saca": [128.50]
        })

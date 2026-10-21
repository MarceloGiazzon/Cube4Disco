import polars as pl

class LocalDataAggregator:
    """
    Agrega transações antes do envio para a nuvem garantindo anonimização (LGPD).
    """
    @staticmethod
    def aggregate_sales_by_geo_and_time(df: pl.DataFrame) -> pl.DataFrame:
        return (
            df.group_by(["codigo_ibge", "semana_safra", "codigo_ncm"])
            .agg([
                pl.col("valor_faturado").sum().alias("total_faturado"),
                pl.col("volume_sacas").sum().alias("total_volume"),
                pl.len().alias("quantidade_transacoes")
            ])
        )

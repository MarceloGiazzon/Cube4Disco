import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

class CausalInferenceEngine:
    """
    Valida relações temporais e elimina correlações espúrias.
    """
    @staticmethod
    def test_granger_causality(series_y: pd.Series, series_x: pd.Series, max_lag: int = 4) -> Dict[str, Any]:
        df = pd.DataFrame({"y": series_y, "x": series_x}).dropna()
        if len(df) <= max_lag * 2:
            return {"valid": False, "reason": "Amostra insuficiente"}

        test_result = grangercausalitytests(df[["y", "x"]], maxlag=max_lag, verbose=False)
        p_values = [test_result[i+1][0]["ssr_ftest"][1] for i in range(max_lag)]
        min_p_value = float(np.min(p_values))

        return {
            "valid": True,
            "granger_causality": min_p_value < 0.05,
            "min_p_value": min_p_value,
            "optimal_lag": int(np.argmin(p_values) + 1)
        }

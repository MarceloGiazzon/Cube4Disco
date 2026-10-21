import pandas as pd
from core.stats.causality import CausalInferenceEngine

def test_granger_causality_with_dummy_data():
    x = pd.Series([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    y = pd.Series([5, 10, 20, 30, 40, 50, 60, 70, 80, 90])
    
    result = CausalInferenceEngine.test_granger_causality(y, x, max_lag=2)
    assert "valid" in result
    assert isinstance(result["valid"], bool)

from typing import Any, Dict

class InsightGenerator:
    """
    Traduz achados causais e coeficientes estatísticos em diagnósticos práticos de negócios.
    """
    @staticmethod
    def format_insight(factor: str, p_value: float, lag: int) -> Dict[str, Any]:
        return {
            "factor": factor,
            "p_value": p_value,
            "defasagem_dias": lag * 7,
            "insight": f"Identificada relação causal significativa onde oscilações em '{factor}' antecipam impactos na operação em {lag} semanas.",
            "recomendacao": "Replanejar posições de estoque e capital de giro antecipando o ciclo meteorológico/mercado."
        }

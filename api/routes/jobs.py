import uuid
from fastapi import APIRouter, status
from api.schemas.requests import CorrelateRequest
from api.schemas.responses import CorrelateAcceptedResponse, JobStatusResponse

router = APIRouter(prefix="/api/v1", tags=["Analise e Correlacao"])

@router.post("/correlate", status_code=status.HTTP_202_ACCEPTED, response_model=CorrelateAcceptedResponse)
async def submit_correlation_analysis(request: CorrelateRequest):
    job_id = f"c4d_{uuid.uuid4().hex[:8]}"
    
    # Disparo assíncrono para workers via Celery
    from workers.tasks import execute_correlation_pipeline
    execute_correlation_pipeline.delay(job_id, request.model_dump())
    
    return CorrelateAcceptedResponse(
        job_id=job_id,
        status="PROCESSING",
        estimated_time_seconds=30,
        check_status_url=f"/api/v1/jobs/{job_id}"
    )

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    # Consulta mock de status; em produção consultar Redis/DB de controle
    return JobStatusResponse(
        job_id=job_id,
        status="COMPLETED",
        findings=[{
            "factor": "precipitacao_acumulada_defasada_21dias",
            "p_value": 0.003,
            "granger_causality": True,
            "relationship": "Atrasos em chuvas superiores a 20 dias reduzem as retiradas imediatas de fertilizantes em 28%.",
            "suggested_action": "Flexibilizar janelas de frete e prazos para adubos de cobertura."
        }]
    )

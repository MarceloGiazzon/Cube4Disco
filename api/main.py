from fastapi import FastAPI
from api.routes import jobs

app = FastAPI(
    title="Cube4Disco API",
    version="1.0.0",
    description="Motor analítico de cubos multidimensionais e causalidade para o Agronegócio."
)

app.include_router(jobs.router)

@app.get("/health", tags=["Infraestrutura"])
def health_check():
    return {"status": "healthy", "service": "Cube4Disco Web Service"}

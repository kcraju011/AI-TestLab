from fastapi import FastAPI

from app.routes.test_routes import router as test_router
from app.routes.batch_routes import router as batch_router
from app.routes.evaluation_routes import router as evaluation_router
from app.routes.rag_routes import router as rag_router
from app.routes.security_routes import router as security_router
from app.routes.reliability_routes import router as reliability_router
from app.routes.regression_routes import router as regression_router

app = FastAPI(
    title="AI-TestLab",
    description=(
        "Automated AI Quality and Reliability "
        "Testing Platform"
    ),
    version="1.0.0"
)


app.include_router(test_router)
app.include_router(batch_router)
app.include_router(evaluation_router)
app.include_router(rag_router)
app.include_router(security_router)
app.include_router(reliability_router)
app.include_router(regression_router)



@app.get("/")
def root():

    return {
        "application": "AI-TestLab",
        "message": "AI Quality Testing Platform is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI-TestLab Backend"
    }
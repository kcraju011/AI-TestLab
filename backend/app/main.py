from fastapi import FastAPI

from app.routes.test_routes import router


app = FastAPI(
    title="AI-TestLab",
    description=(
        "Automated AI Quality and Reliability "
        "Testing Platform"
    ),
    version="1.0.0"
)


app.include_router(router)


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
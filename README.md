# AI-TestLab – AI Quality, Security & Reliability Testing Platform

AI-TestLab is a Python-based platform for evaluating the quality, reliability, security and regression behavior of Large Language Model (LLM) applications.

It provides automated test execution, RAG evaluation, security scanning, performance measurements and historical analytics through a React dashboard.

## Key Features

- **LLM Quality Evaluation:** Evaluate answer relevancy, faithfulness and hallucination-related metrics.
- **RAG Evaluation:** Test retrieval quality and the relationship between retrieved context and generated answers.
- **AI Security Testing:** Test for prompt injection patterns and potential sensitive-information exposure.
- **Reliability Testing:** Measure request success, failures and response latency.
- **Regression Testing:** Compare test outcomes across runs to identify quality regressions.
- **Historical Analytics:** Store test runs and individual test-case results in PostgreSQL.
- **Dashboard:** Visualize test results, quality indicators and historical performance.
- **Automated CI:** Run backend tests and frontend builds through GitHub Actions.

## Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, FastAPI |
| AI evaluation | DeepEval |
| LLM integration | OpenAI API |
| RAG | SentenceTransformers, ChromaDB |
| Database | PostgreSQL, SQLAlchemy, Alembic |
| Frontend | React, Vite |
| Testing | Pytest, HTTPX |
| Infrastructure | Docker, Docker Compose |
| CI | GitHub Actions |

## Architecture

React Dashboard → FastAPI → Evaluation and Testing Services → PostgreSQL

The platform also integrates with an LLM provider and a local vector store for retrieval-augmented generation experiments.

## Run Locally with Docker

1. Configure the root `.env` file with `POSTGRES_PASSWORD`.
2. Configure `backend/.env` with the required application settings and LLM credentials.
3. Ensure your database schema has been migrated.
4. Build and start the services:

```powershell
docker compose build
docker compose up -d
```

## Application URLs

- Frontend: http://localhost:8081
- API: http://localhost:8000
- Swagger documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Run Backend Tests

```powershell
cd backend
pytest -v
```

## Project Structure

```text
AI-TestLab/
├── backend/
├── frontend/
├── reports/
├── .github/workflows/
├── docker-compose.yml
└── README.md
```

## Testing Philosophy

AI-TestLab combines deterministic test cases, metric-based evaluation and automated regression checks. LLM-as-a-judge metrics can be variable and should be interpreted alongside repeatability checks and human review.

Security scanners use defined detection patterns and are not a substitute for a comprehensive security control system.

## Future Improvements

- More robust adversarial test datasets.
- Additional LLM provider integrations.
- Versioned evaluation datasets.
- Advanced regression comparison and alerting.
- Role-based access control and audit logging.
- Production deployment with managed database and monitoring.

## Author

Raju Chavan

Computer Science Graduate | Python | Java | Backend Development | AI Quality Engineering
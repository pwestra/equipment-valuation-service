# Equipment Valuation Service

A small, production-style REST API for calculating equipment market and auction values based on classification ID and model year.

This project was implemented as a take-home exercise with an emphasis on:

- Clean architecture  
- Testability  
- Reproducibility  
- Realistic team workflow (Gitflow)  
- Clear documentation  

---

# Overview

The service exposes an HTTP endpoint that:

1) Looks up classification data from a JSON dataset  
2) Applies year-specific valuation ratios  
3) Returns rounded market and auction values  

The API is implemented using FastAPI.

---

# Tech Stack

- Python 3.11+  
- FastAPI  
- Pydantic  
- Pytest  
- Uvicorn  
- Docker  

---

# Project Structure

src/
  valuation_service/
    api/            → HTTP routes
    domain/         → core models
    repositories/   → data access layer
    services/       → business logic

tests/              → unit tests

This follows a layered architecture separating:

- API layer  
- Domain models  
- Business logic  
- Data access  

---

# Instructions for Building, Compiling, and Deploying the Service

You can run the service in two ways.

---

## Recommended: Docker (most portable)

Prerequisite: Docker Desktop (Windows/macOS) or Docker Engine (Linux)

Build:

```bash
docker build -t valuation-service:latest .
```

Run:

```bash
docker run -p 8000:8000 valuation-service:latest
```

Service will be available at:

http://localhost:8000

Swagger UI:

http://localhost:8000/docs

---

## Alternative: Native Python

Prerequisite: Python 3.11+

With this alternative method I suggest using a virtual environment to avoid 
affecting local python installations

Linux / macOS / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn valuation_service.main:app --app-dir src --reload --port 8000
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn valuation_service.main:app --app-dir src --reload --port 8000
```

---

# Instructions for How to Call the Service

Endpoint:

GET /v1/valuations/{classification_id}?year={model_year}

Example:

```bash
curl "http://127.0.0.1:8000/v1/valuations/87390?year=2016"
```

Example Response:

{
  "classification_id": 87390,
  "model_year": 2016,
  "market_value": 30008,
  "auction_value": 20426,
  "currency": "USD"
}

---

# Running Tests

```bash
pytest -q
```

---

# Data File

The service reads:

api-response.json

Default location: repository root.

Optional override:

Linux/macOS/WSL:

```bash
export BOOK_JSON_PATH=./api-response.json
```

Windows PowerShell:

```powershell
$env:BOOK_JSON_PATH = ".\api-response.json"
```

---

# Explanation of Design Patterns

The implementation uses several common backend design patterns to keep the system clean and maintainable.

Repository Pattern:

The ClassificationRepository abstracts data access.

Benefits:
- API does not depend on JSON structure  
- Easy to swap in database later  
- Improves testability  

Service Layer Pattern:

ValuationService contains business logic.

Benefits:
- Separates business rules from HTTP layer  
- Keeps routes thin  
- Easy unit testing  

Dependency Injection:

FastAPI dependency injection is used to provide the service to routes.

Benefits:
- Easy to mock in tests  
- Loose coupling  
- Clean separation of concerns  

Layered Architecture:

API → Services → Repositories → Data

Benefits:
- Clear responsibilities  
- Easier maintenance  
- Realistic production structure  

---

# Gitflow Workflow

This project follows a simplified Gitflow model:

- main → production-ready code  
- develop → integration branch  
- feature/* → feature development  
- release/* → release preparation  

This mirrors team-based development workflows.

---

# Notes

- Values are rounded to nearest integer  
- JSON schema assumed valid for this exercise  
- Swagger UI enabled for convenience  

---

# Author

Peter Westra

## Gitflow
This repo uses a simplified Gitflow model.

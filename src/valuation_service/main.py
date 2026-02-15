from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI

from valuation_service.api.routes import get_service, router
from valuation_service.repositories.classification_repo import (
    ApiResponseJsonClassificationRepository,
)
from valuation_service.services.valuation import ValuationService

app = FastAPI(title="Equipment Valuation Service", version="1.0.0")

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[2] / "api-response.json"
DATA_PATH = Path(os.getenv("BOOK_JSON_PATH", str(DEFAULT_DATA_PATH)))

_repo = ApiResponseJsonClassificationRepository(DATA_PATH)
_svc = ValuationService(_repo)


def _get_service_override() -> ValuationService:
    return _svc


app.dependency_overrides[get_service] = _get_service_override
app.include_router(router)

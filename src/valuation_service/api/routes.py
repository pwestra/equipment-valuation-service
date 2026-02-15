from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from valuation_service.services.valuation import (
    MissingRatioError,
    UnknownClassificationError,
    ValuationResult,
    ValuationService,
    YearOutOfRangeError,
)

router = APIRouter()


class ValuationResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    classification_id: int
    model_year: int
    market_value: int
    auction_value: int
    currency: str


def get_service() -> ValuationService:
    """
    Dependency injection hook.
    Overridden in tests and wired in main.py.
    """
    raise RuntimeError("ValuationService dependency not configured")


@router.get("/v1/valuations/{classification_id}", response_model=ValuationResponse)
def get_valuation(
    classification_id: int,
    year: int = Query(..., description="Model year (2006–2020 inclusive)"),
    svc: ValuationService = Depends(get_service),
):
    try:
        result: ValuationResult = svc.compute(classification_id, year)
        return ValuationResponse(**result.__dict__)

    except YearOutOfRangeError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except UnknownClassificationError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    except MissingRatioError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

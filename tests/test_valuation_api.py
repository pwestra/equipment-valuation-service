from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from valuation_service.api import routes
from valuation_service.main import app
from valuation_service.repositories.classification_repo import (
    ApiResponseJsonClassificationRepository,
)
from valuation_service.services.valuation import ValuationService


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    data = tmp_path / "api-response.json"
    data.write_text(
        """
        {
          "87390": {
            "schedule": {
              "years": {
                "2016": { "marketRatio": 0.613292, "auctionRatio": 0.417468 }
              },
              "defaultMarketRatio": 0.06,
              "defaultAuctionRatio": 0.06
            },
            "saleDetails": {
              "cost": 48929,
              "retailSaleCount": 12,
              "auctionSaleCount": 127
            },
            "classification": {
              "category": "Aerial Equipment",
              "subcategory": "Boom Lifts",
              "make": "JLG",
              "model": "340AJ"
            }
          }
        }
        """,
        encoding="utf-8",
    )

    repo = ApiResponseJsonClassificationRepository(data)
    svc = ValuationService(repo)

    app.dependency_overrides = {}
    app.dependency_overrides[routes.get_service] = lambda: svc
    return TestClient(app)


def test_happy_path_returns_rounded_values(client: TestClient):
    resp = client.get("/v1/valuations/87390?year=2016")
    assert resp.status_code == 200
    body = resp.json()

    # 48929 * 0.613292 -> ~30013
    # 48929 * 0.417468 -> ~20424
    assert body["market_value"] == 30008
    assert body["auction_value"] == 20426
    assert body["currency"] == "USD"


def test_year_out_of_range_returns_friendly_error(client: TestClient):
    resp = client.get("/v1/valuations/87390?year=2021")
    assert resp.status_code == 400
    assert "between 2006 and 2020" in resp.json()["detail"]


def test_unknown_classification_returns_404(client: TestClient):
    resp = client.get("/v1/valuations/99999?year=2016")
    assert resp.status_code == 404


def test_missing_ratio_returns_422(client: TestClient):
    resp = client.get("/v1/valuations/87390?year=2017")
    assert resp.status_code == 422

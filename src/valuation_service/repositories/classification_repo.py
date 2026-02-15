from __future__ import annotations

import json
from pathlib import Path

from valuation_service.domain.models import Classification, RatioSet


class ClassificationRepository:
    def get(self, classification_id: int) -> Classification | None:
        raise NotImplementedError


class ApiResponseJsonClassificationRepository(ClassificationRepository):
    """
    Exact api-response.json schema (assumed valid; minimal handling):

      root: { "<classification_id>": { ... }, ... }

      cost:
        payload["saleDetails"]["cost"]

      ratios:
        payload["schedule"]["years"]["<YYYY>"]["marketRatio"]
        payload["schedule"]["years"]["<YYYY>"]["auctionRatio"]

      metadata:
        payload.get("classification")
    """

    def __init__(self, json_path: Path):
        self._json_path = json_path
        self._cache: dict[int, Classification] = {}
        self._loaded = False

    def _load_if_needed(self) -> None:
        if self._loaded:
            return

        raw = json.loads(self._json_path.read_text(encoding="utf-8"))

        for cid_str, payload in raw.items():
            cid = int(cid_str)

            cost = float(payload["saleDetails"]["cost"])

            ratios_by_year: dict[int, RatioSet] = {}
            years_obj = payload["schedule"]["years"]
            for year_str, year_payload in years_obj.items():
                year = int(year_str)
                market_ratio = float(year_payload["marketRatio"])
                auction_ratio = float(year_payload["auctionRatio"])
                ratios_by_year[year] = RatioSet(market=market_ratio, auction=auction_ratio)

            hierarchy = payload.get("classification")

            self._cache[cid] = Classification(
                classification_id=cid,
                book_cost=cost,
                ratios_by_year=ratios_by_year,
                hierarchy=hierarchy,
            )

        self._loaded = True

    def get(self, classification_id: int) -> Classification | None:
        self._load_if_needed()
        return self._cache.get(classification_id)

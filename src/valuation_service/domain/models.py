from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RatioSet:
    market: float
    auction: float


@dataclass(frozen=True)
class Classification:
    classification_id: int
    book_cost: float  # we reuse the field name; it will store "saleDetails.cost"
    ratios_by_year: dict[int, RatioSet]
    hierarchy: dict | None = None

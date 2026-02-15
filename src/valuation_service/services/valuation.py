from __future__ import annotations

from dataclasses import dataclass

from valuation_service.repositories.classification_repo import ClassificationRepository

MIN_YEAR = 2006
MAX_YEAR = 2020


class ValuationError(Exception):
    pass


class YearOutOfRangeError(ValuationError):
    pass


class UnknownClassificationError(ValuationError):
    pass


class MissingRatioError(ValuationError):
    pass


@dataclass(frozen=True)
class ValuationResult:
    classification_id: int
    model_year: int
    market_value: int
    auction_value: int
    currency: str = "USD"


class ValuationService:
    def __init__(self, repo: ClassificationRepository):
        self._repo = repo

    def compute(self, classification_id: int, model_year: int) -> ValuationResult:
        if model_year < MIN_YEAR or model_year > MAX_YEAR:
            raise YearOutOfRangeError(
                f"Model Year must be between {MIN_YEAR} and {MAX_YEAR} (inclusive)."
            )

        classification = self._repo.get(classification_id)
        if classification is None:
            raise UnknownClassificationError(f"Unknown classification_id={classification_id}.")

        ratios = classification.ratios_by_year.get(model_year)
        if ratios is None:
            raise MissingRatioError(
                f"No ratios found for classification_id={classification_id} "
                f"and model_year={model_year}."
            )

        market_value = int(round(classification.book_cost * ratios.market))
        auction_value = int(round(classification.book_cost * ratios.auction))

        return ValuationResult(
            classification_id=classification_id,
            model_year=model_year,
            market_value=market_value,
            auction_value=auction_value,
        )

from __future__ import annotations

from typing import TYPE_CHECKING
from .inventory import Inventory
from .query import Filter, Projection

if TYPE_CHECKING:
    import pandas as pd


class InventoryData:
    def __init__(self) -> None:
        pass

    @classmethod
    def from_inventory(cls, inventory: Inventory) -> InventoryData:
        pass

    @classmethod
    def from_csv(cls, path: str, mapping: dict, kind: str) -> InventoryData:
        pass

    @classmethod
    def from_api(cls, url: str, mapping: dict, kind: str, *, records_path: str | None = None) -> InventoryData:
        pass

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, mapping: dict, kind: str) -> InventoryData:
        pass

    def get_products(self, filter: Filter | None = None, projection: Projection | None = None) -> pd.DataFrame:
        pass

    def get_events(self, filter: Filter | None = None, projection: Projection | None = None) -> pd.DataFrame:
        pass

    def get_stock_at(self, timestamp: str, filter: Filter | None = None) -> pd.DataFrame:
        pass

    def clean(self) -> None:
        pass

    def validate(self) -> dict:
        pass

    def refresh(self) -> None:
        pass

    def _load_csv(self, path: str) -> pd.DataFrame:
        pass

    def _fetch_api(self, url: str) -> dict | list:
        pass

    def _extract_json_records(self, data: dict | list, records_path: str | None = None) -> list[dict]:
        pass

    def _query_inventory_products(self, filter: Filter | None, projection: Projection | None) -> list[dict]:
        pass

    def _query_inventory_events(self, filter: Filter | None, projection: Projection | None) -> list[dict]:
        pass

    def _products_to_dataframe(self, products: list) -> pd.DataFrame:
        pass

    def _events_to_dataframe(self, events: list) -> pd.DataFrame:
        pass

    def _rename_columns(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        pass

    def _normalize_types(self, df: pd.DataFrame, kind: str) -> pd.DataFrame:
        pass

    def _normalize_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def _normalize_event_types(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def _handle_missing_values(self, df: pd.DataFrame, kind: str) -> pd.DataFrame:
        pass

    def _handle_duplicates(self, df: pd.DataFrame, kind: str) -> pd.DataFrame:
        pass

    def _validate_schema(self, df: pd.DataFrame, kind: str) -> None:
        pass

    def _validate_references(self, products: pd.DataFrame, events: pd.DataFrame) -> None:
        pass

    def _filter_dataframe(self, df: pd.DataFrame, filter: Filter | None) -> pd.DataFrame:
        pass

    def _project_dataframe(self, df: pd.DataFrame, projection: Projection | None) -> pd.DataFrame:
        pass


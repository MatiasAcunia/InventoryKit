from __future__ import annotations

from typing import TYPE_CHECKING
from .data import InventoryData

if TYPE_CHECKING:
    import pandas as pd


class InventoryStatistics:
    def __init__(self, data: InventoryData) -> None:
        pass

    def top_products(self, start: str, end: str, limit: int = 10) -> pd.DataFrame:
        pass

    def least_sold_products(self, start: str, end: str, limit: int = 10) -> pd.DataFrame:
        pass

    def stock_turnover(self, start: str, end: str) -> pd.DataFrame:
        pass

    def dead_stock(self, days: int) -> pd.DataFrame:
        pass

    def sales_by_period(self, start: str, end: str, frequency: str = "D") -> pd.DataFrame:
        pass

    def peak_periods(self, start: str, end: str, frequency: str = "D") -> pd.DataFrame:
        pass

    def movement_summary(self, start: str, end: str) -> pd.DataFrame:
        pass

    def stock_evolution(self, start: str, end: str) -> pd.DataFrame:
        pass

    def inventory_value(self) -> pd.DataFrame:
        pass

    def abc_analysis(self, start: str, end: str, a_threshold: float = 0.8, b_threshold: float = 0.95) -> pd.DataFrame:
        pass

    def minimum_stock(self, start: str, end: str, safety_days: int = 0) -> pd.DataFrame:
        pass

    def restock_recommendations(self, start: str, end: str, coverage_days: int, safety_days: int = 0) -> pd.DataFrame:
        pass

    def _require_columns(self, df: pd.DataFrame, columns: list[str]) -> None:
        pass

    def _validate_period(self, start: str, end: str) -> None:
        pass

    def _get_sales(self, start: str, end: str) -> pd.DataFrame:
        pass

    def _get_movements(self, start: str, end: str) -> pd.DataFrame:
        pass

    def _get_current_stock(self) -> pd.DataFrame:
        pass

    def _get_initial_stock(self, start: str) -> pd.DataFrame:
        pass

    def _group_by_product(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def _group_by_period(self, df: pd.DataFrame, frequency: str) -> pd.DataFrame:
        pass

    def _merge_product_information(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def _calculate_daily_demand(self, sales: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
        pass

    def _calculate_average_stock(self, stock: pd.DataFrame) -> pd.DataFrame:
        pass

    def _calculate_revenue(self, sales: pd.DataFrame) -> pd.DataFrame:
        pass

    def _calculate_inventory_cost(self, products: pd.DataFrame) -> pd.DataFrame:
        pass

    def _calculate_cumulative_percentage(self, revenue: pd.DataFrame) -> pd.DataFrame:
        pass

    def _classify_abc(self, revenue: pd.DataFrame, a_threshold: float, b_threshold: float) -> pd.DataFrame:
        pass

    def _calculate_reorder_point(self, demand: pd.DataFrame, safety_days: int) -> pd.DataFrame:
        pass

    def _calculate_restock_quantity(self, demand: pd.DataFrame, coverage_days: int, safety_days: int) -> pd.DataFrame:
        pass


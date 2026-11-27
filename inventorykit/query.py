class Filter:
    def __init__(self, conditions: dict) -> None:
        pass

    def _validate_structure(self, conditions: dict) -> None:
        pass

    def _validate_operator(self, operator: str) -> None:
        pass

    def _validate_operand(self, operator: str, value) -> None:
        pass

    def _parse_conditions(self, conditions: dict) -> dict:
        pass

    def to_dict(self) -> dict:
        pass


class Projection:
    def __init__(self, fields: dict) -> None:
        pass

    def _validate_fields(self, fields: dict) -> None:
        pass

    def _validate_mode(self, fields: dict) -> None:
        pass

    def to_dict(self) -> dict:
        pass


class Sort:
    def __init__(self, fields: dict) -> None:
        pass

    def _validate_fields(self, fields: dict) -> None:
        pass

    def _validate_direction(self, direction: int) -> None:
        pass

    def to_dict(self) -> dict:
        pass


class _QueryCompiler:
    def _resolve_field(self, field: str, entity: str) -> str:
        pass

    def _compile_filter(self, filter: Filter | None, entity: str) -> tuple[str, list]:
        pass

    def _compile_condition(self, field: str, operator: str, value, entity: str) -> tuple[str, list]:
        pass

    def _compile_logical(self, operator: str, conditions: list, entity: str) -> tuple[str, list]:
        pass

    def _compile_projection(self, projection: Projection | None, entity: str) -> str:
        pass

    def _compile_sort(self, sort: Sort | None, entity: str) -> str:
        pass

    def _compile_pagination(self, limit: int | None, skip: int) -> tuple[str, list]:
        pass

    def _compile_query(self, entity: str, filter: Filter | None = None, projection: Projection | None = None, sort: Sort | None = None, limit: int | None = None, skip: int = 0, include_inactive: bool = False) -> tuple[str, list]:
        pass


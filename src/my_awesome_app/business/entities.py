from __future__ import annotations
import operator

from decimal import Decimal

from pydantic.dataclasses import dataclass

from my_awesome_app.business.value_objects import Operation


@dataclass(kw_only=True)
class OperationExecution:
    id: int | None
    a: Decimal
    operation: Operation
    b: Decimal
    result: Decimal

    @classmethod
    def calculate(
        cls,
        *,
        a: Decimal,
        operation: Operation,
        b: Decimal,
        raise_error_on_div_by_zero: bool,
    ) -> OperationExecution:
        func = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow,
        }[operation]
        try:
            result = func(a, b)
        except ZeroDivisionError:
            if raise_error_on_div_by_zero:
                raise
            result = Decimal("0")

        return OperationExecution(id=None, a=a, operation=operation, b=b, result=result)

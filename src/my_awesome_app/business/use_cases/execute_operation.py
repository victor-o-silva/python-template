from decimal import Decimal

from my_awesome_app.business.entities import OperationExecution
from my_awesome_app.business.value_objects import Operation


class ExecuteOperationUseCase:
    def __init__(self, *, raise_error_on_div_by_zero: bool):
        self.raise_error_on_div_by_zero = raise_error_on_div_by_zero

    async def run(self, *, a: Decimal, operation: Operation, b: Decimal) -> OperationExecution:
        execution = OperationExecution.calculate(
            a=a,
            operation=operation,
            b=b,
            raise_error_on_div_by_zero=self.raise_error_on_div_by_zero,
        )
        return execution

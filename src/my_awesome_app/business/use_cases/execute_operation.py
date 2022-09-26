from decimal import Decimal
from logging import getLogger

from my_awesome_app.business.entities import OperationExecution
from my_awesome_app.business.interfaces import IUnitOfWorkMaker
from my_awesome_app.business.value_objects import Operation

logger = getLogger(__name__)


class ExecuteOperationUseCase:
    def __init__(self, *, uow_maker: IUnitOfWorkMaker, raise_error_on_div_by_zero: bool):
        self.uow_maker = uow_maker
        self.raise_error_on_div_by_zero = raise_error_on_div_by_zero

    async def run(self, *, a: Decimal, operation: Operation, b: Decimal) -> OperationExecution:
        execution = OperationExecution.calculate(
            a=a,
            operation=operation,
            b=b,
            raise_error_on_div_by_zero=self.raise_error_on_div_by_zero,
        )
        async with await self.uow_maker() as unit_of_work:
            await unit_of_work.operation_repository.persist_operation(operation_execution=execution)
            logger.info('Persisted %s', execution)

        return execution

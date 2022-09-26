from my_awesome_app.business.entities import OperationExecution
from my_awesome_app.business.interfaces import IUnitOfWorkMaker
from my_awesome_app.business.utils import GenericPage


class ListOperationUseCase:
    def __init__(self, *, uow_maker: IUnitOfWorkMaker):
        self.uow_maker = uow_maker

    async def run(self, *, limit: int, offset: int) -> GenericPage[OperationExecution]:
        async with await self.uow_maker() as unit_of_work:
            return await unit_of_work.operation_repository.list_operations(limit=limit, offset=offset)

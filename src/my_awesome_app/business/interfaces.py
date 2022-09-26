from __future__ import annotations

from my_awesome_app.business.entities import OperationExecution
from my_awesome_app.business.utils import GenericPage


class IOperationRepository:
    async def get_operation(self, operation_execution_id: int, *, for_update: bool = False) -> OperationExecution:
        raise NotImplementedError

    async def list_operations(self, *, limit: int, offset: int) -> GenericPage[OperationExecution]:
        raise NotImplementedError

    async def persist_operation(self, operation_execution: OperationExecution):
        raise NotImplementedError


class IUnitOfWork:
    operation_repository: IOperationRepository

    async def __aenter__(self) -> IUnitOfWork:
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_value:
            await self.rollback()
            raise exc_value

        await self.commit()

    async def commit(self):
        raise NotImplementedError()

    async def rollback(self):
        raise NotImplementedError()


class IUnitOfWorkMaker:
    async def __call__(self) -> IUnitOfWork:
        raise NotImplementedError()

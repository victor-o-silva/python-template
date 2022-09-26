from logging import getLogger

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from my_awesome_app.business.entities import OperationExecution
from my_awesome_app.business.interfaces import IOperationRepository
from my_awesome_app.business.utils import GenericPage
from my_awesome_app.infrastructure.orm.models import OperationModel

logger = getLogger(__name__)


class SqlAlchemyOperationRepository(IOperationRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def list_operations(self, *, limit: int, offset: int) -> GenericPage[OperationExecution]:
        statement = select(OperationModel)

        total_count_statement = statement.with_only_columns(func.count(OperationModel.id)).order_by(None)
        total_count = (await self.db_session.execute(total_count_statement)).scalar_one()

        statement = statement.limit(limit).offset(offset)
        rows = [r[0] for r in (await self.db_session.execute(statement)).fetchall()]

        return GenericPage[OperationExecution](
            data=[
                OperationExecution(
                    id=row.id,
                    a=row.a,
                    operation=row.operation,
                    b=row.b,
                    result=row.result,
                )
                for row in rows
            ],
            total_items=total_count,
        )

    async def persist_operation(self, operation_execution: OperationExecution):
        model = OperationModel(
            a=operation_execution.a,
            operation=operation_execution.operation,
            b=operation_execution.b,
            result=operation_execution.result
        )
        self.db_session.add(model)
        await self.db_session.flush()

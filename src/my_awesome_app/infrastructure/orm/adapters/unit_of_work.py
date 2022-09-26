from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from my_awesome_app.business.interfaces import IUnitOfWork
from my_awesome_app.infrastructure.orm.adapters.operation_repository import SqlAlchemyOperationRepository


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, db_session_maker: sessionmaker):
        self.db_session_maker = db_session_maker

    async def __aenter__(self) -> IUnitOfWork:
        self.db_session: AsyncSession = self.db_session_maker()
        self.operation_repository = SqlAlchemyOperationRepository(db_session=self.db_session)
        return self

    async def commit(self):
        await self.db_session.commit()

    async def rollback(self):
        await self.db_session.rollback()

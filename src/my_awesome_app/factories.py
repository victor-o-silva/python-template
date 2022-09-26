from sqlalchemy.orm import sessionmaker

from my_awesome_app.business.interfaces import IUnitOfWorkMaker
from my_awesome_app.infrastructure.orm.adapters.unit_of_work import SqlAlchemyUnitOfWork
from my_awesome_app.infrastructure.orm.session_maker import get_async_session_maker
from my_awesome_app.settings import Settings


def get_settings() -> Settings:
    return Settings()


async def get_db_session_maker() -> sessionmaker:
    return await get_async_session_maker()


async def get_unit_of_work_maker(*, db_session_maker: sessionmaker) -> IUnitOfWorkMaker:
    class UOWMaker(IUnitOfWorkMaker):
        async def __call__(self):
            return SqlAlchemyUnitOfWork(db_session_maker=db_session_maker)

    return UOWMaker()

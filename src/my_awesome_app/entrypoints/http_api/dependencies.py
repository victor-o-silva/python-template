from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from my_awesome_app import factories
from my_awesome_app.business.interfaces import IUnitOfWorkMaker
from my_awesome_app.settings import Settings


def get_settings() -> Settings:
    return factories.get_settings()


async def get_unit_of_work_maker(
    db_session_maker: sessionmaker = Depends(factories.get_db_session_maker),
) -> IUnitOfWorkMaker:
    return await factories.get_unit_of_work_maker(db_session_maker=db_session_maker)


import logging
import os
from contextlib import suppress

import alembic
import alembic.config
import pytest
from sqlalchemy.orm import sessionmaker

from my_awesome_app.business.interfaces import IUnitOfWorkMaker
from my_awesome_app.infrastructure.orm.adapters.unit_of_work import SqlAlchemyUnitOfWork
from my_awesome_app.infrastructure.orm.session_maker import get_async_session_maker
from my_awesome_app.settings import Settings


@pytest.fixture
def repository_root(request) -> str:
    return os.path.dirname(os.path.dirname(os.path.realpath(request.config.rootdir)))


@pytest.fixture
def database_path(repository_root: str) -> str:
    return os.path.join(repository_root, 'src', 'unit_tests', 'test_database.sqlite')


@pytest.fixture()
def settings(database_path: str) -> Settings:
    return Settings(
        DATABASE_URL=f'sqlite+aiosqlite:///{database_path}',
    )


@pytest.fixture()
async def sql_alchemy_session_maker(
    monkeypatch, database_path, repository_root: str, settings: Settings
) -> sessionmaker:
    logging.getLogger('alembic.runtime.migration').disabled = True
    monkeypatch.setenv('DATABASE_URL', settings.DATABASE_URL)
    with suppress(FileNotFoundError):
        os.remove(database_path)

    # Run migrations
    alembic_ini_path = os.path.join(repository_root, 'alembic_migrations/alembic.ini')
    config = alembic.config.Config(alembic_ini_path)
    alembic_migrations_path = os.path.join(repository_root, 'alembic_migrations')
    config.set_main_option('script_location', alembic_migrations_path)
    alembic.command.upgrade(config, 'head')

    # Async session
    session_maker = await get_async_session_maker()
    yield session_maker
    with suppress(FileNotFoundError):
        os.remove(database_path)


@pytest.fixture()
async def sql_alchemy_uow_maker(sql_alchemy_session_maker: sessionmaker) -> IUnitOfWorkMaker:
    class UOWMaker(IUnitOfWorkMaker):
        async def __call__(self):
            return SqlAlchemyUnitOfWork(db_session_maker=sql_alchemy_session_maker)

    return UOWMaker()

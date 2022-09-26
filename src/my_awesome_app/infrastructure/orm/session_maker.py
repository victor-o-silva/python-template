import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

async_engine: AsyncEngine | None = None


async def get_async_session_maker() -> sessionmaker:
    global async_engine
    if not async_engine:
        database_url = os.getenv('DATABASE_URL')
        engine_kwargs = {
            'echo': os.getenv('ECHO_SQL', '').lower() in {'1', 'true', 'on'},
            'future': True,  # enable 2.0 style (https://docs.sqlalchemy.org/en/14/glossary.html#term-2.0-style)
        }
        if 'sqlite' not in database_url:  # pragma: no cover
            engine_kwargs.update(isolation_level='READ COMMITTED', pool_size=20, pool_recycle=3600)

        async_engine = create_async_engine(database_url, **engine_kwargs)

    maker = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return maker

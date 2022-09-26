import os
from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic import context
from my_awesome_app.infrastructure.orm.base_model import BaseOrmModel
from my_awesome_app.infrastructure.orm.models import *  # noqa: F401,F403

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseOrmModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_db_url() -> str:
    """
    The application connects to the database using async drivers.
    Our Alembic instance, however, doesn't. So we remove the async driver from the connection string.
    """
    database_url = os.getenv('DATABASE_URL')

    if database_url.startswith('sqlite'):
        database_url = database_url.replace('sqlite+aiosqlite:', 'sqlite:')
    elif database_url.startswith('postgresql'):
        database_url = database_url.replace('postgresql+asyncpg:', 'postgresql+psycopg2:')
    else:
        dialect = database_url.split(':')[0].split('+')[0]
        raise RuntimeError(f'Unexpected database dialect: {dialect}')

    return database_url


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    database_url = get_db_url()
    config.set_main_option('sqlalchemy.url', database_url)
    connectable = create_engine(database_url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

import os

from fastapi import FastAPI

from my_awesome_app.entrypoints.http_api.router import main_router
from my_awesome_app.factories import get_settings
from my_awesome_app.logging_conf import configure_logging


logging_args = {'root_level': 'INFO', 'uvicorn_level': 'INFO', 'project_level': 'INFO'}
if not os.environ.get('PYTEST_CURRENT_TEST'):
    settings = get_settings()
    logging_args.update(
        root_level=settings.LOG_LEVEL_ROOT,
        uvicorn_level=settings.LOG_LEVEL_UVICORN,
        project_level=settings.LOG_LEVEL_PROJECT,
    )
configure_logging(**logging_args)

app = FastAPI(
    title='my_awesome_app',
    debug=os.environ.get('DEBUG', '').lower() in {'true', 'on', '1'},
)

app.include_router(main_router)

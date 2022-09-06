from pydantic import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL_ROOT: str = 'INFO'
    LOG_LEVEL_UVICORN: str = 'INFO'
    LOG_LEVEL_PROJECT: str = 'INFO'
    RAISE_ERROR_ON_DIVISION_BY_ZERO: bool = True

import pytest

from my_awesome_app.settings import Settings


@pytest.fixture()
def settings() -> Settings:
    return Settings()

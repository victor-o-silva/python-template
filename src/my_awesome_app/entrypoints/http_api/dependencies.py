from my_awesome_app import factories
from my_awesome_app.settings import Settings


def get_settings() -> Settings:
    return factories.get_settings()


import logging.config
import sys


def configure_logging(*, root_level: str, uvicorn_level: str, project_level: str):
    config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                '()': 'colorlog.ColoredFormatter',
                'format': '%(log_color)s%(asctime)s [%(levelname)-8s] %(name)s:L%(lineno)d%(reset)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z',
            },
        },
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout,
            },
        },
        'loggers': {
            '': {
                'handlers': [
                    'default',
                ],
                'level': root_level,
                'propagate': True,
            },
            'uvicorn': {
                'handlers': [
                    'default',
                ],
                'level': uvicorn_level,
                'propagate': False,
            },
            'my_awesome_app': {
                'handlers': [
                    'default',
                ],
                'level': project_level,
                'propagate': False,
            },
        },
    }
    logging.config.dictConfig(config)

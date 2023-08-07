import logging as log
import pathlib

from pydantic import BaseSettings
from colorama import Fore


class LoggingConfig(BaseSettings):
    pathlib.Path('cache/').mkdir(parents=True, exist_ok=True)

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "cache/logs.log"
    LOG_FORMAT: str = (
        "[%(asctime)s]:"
        "[%(levelname)-11s]:"
        "[LINE:%(lineno)-4s]:"
        "[%(name)s]:"
        "[%(filename)s]:::"
        "%(message)s"
    )
    LOG_FORMAT_COLORS: str = (
            Fore.BLUE + "[%(asctime)s]:"
            + Fore.CYAN + "[%(levelname)-11s]:"
            + Fore.WHITE + "[LINE:%(lineno)-4s]:"
            + Fore.GREEN + "[%(name)s]:"
            + Fore.MAGENTA + "[%(filename)s]:::"
            + Fore.WHITE + "%(message)s"
    )

    class Config:
        env_file = ".env"


def configure_logger():
    basic_formatter = log.Formatter(LOG_CONF.LOG_FORMAT)
    colored_formatter = log.Formatter(LOG_CONF.LOG_FORMAT_COLORS)

    file_handler = log.FileHandler(LOG_CONF.LOG_FILE)
    file_handler.setFormatter(basic_formatter)

    std_handler = log.StreamHandler()
    std_handler.setFormatter(colored_formatter)

    logger = log.getLogger()
    log.addLevelName(15, "USER ACTION")
    logger.setLevel("USER ACTION")
    logger.addHandler(file_handler)
    logger.addHandler(std_handler)


LOG_CONF = LoggingConfig()
configure_logger()

import dataclasses
import logging
import os
import sys
from typing import Any

from minosreports.constants import (
    NAME,
)

DEFAULT_FORMAT_WITH_THREADS = (
    "[%(name)s::%(threadName)s::%(asctime)s] %(levelname)s:%(message)s"
)
VERBOSE_DEPENDENCIES = ["urllib3", "PIL", "boto3", "botocore", "s3transfer"]


def getLogger(  # noqa: N802 (intentionally matches the stdlib getLogger name)
    name: str,
    log_format: str,
    level: int = logging.INFO,
):
    """configured logger for most usages"""

    # set arbitrary level for some known verbose dependencies
    # prevents them from polluting logs
    for logger_name in set(VERBOSE_DEPENDENCIES):
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    logger = logging.Logger(name)
    logger.setLevel(logging.DEBUG)

    # setup console logging
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    return logger


@dataclasses.dataclass(kw_only=True)
class Context:
    """Class holding every contextual / configuration bits which can be moved

    Used to easily pass information around in the scraper. One singleton instance is
    always available.
    """

    # singleton instance
    _instance: "Context | None" = None

    # debug flag
    debug: bool = False

    # logger to use everywhere (do not mind about mutability, we want to reuse same
    # logger everywhere)
    logger: logging.Logger = getLogger(  # noqa: RUF009
        NAME, level=logging.DEBUG, log_format=DEFAULT_FORMAT_WITH_THREADS
    )

    database_url: str = os.getenv("POSTGRES_URI", "")  # noqa: RUF009

    if not database_url:
        raise Exception("POSTGRES_URI environment variable is mandatory")

    supervisor_mails: list[str] = os.getenv(  # noqa: RUF009
        "SUPERVISOR_MAILS", ""
    ).split(",")

    if not supervisor_mails:
        raise Exception("SUPERVISOR_MAILS environment variable is mandatory")

    dlus_mails: list[str] = os.getenv("DLUS_MAILS", "").split(",")  # noqa: RUF009

    if not dlus_mails:
        raise Exception("DLUS_MAILS environment variable is mandatory")

    api_root_path: str = os.getenv("API_ROOT_PATH", "")  # noqa: RUF009

    @classmethod
    def setup(cls, **kwargs: Any):
        new_instance = cls(**kwargs)
        if cls._instance:
            # replace values 'in-place' so that we do not change the Context object
            # which might be already imported in some modules
            for field in dataclasses.fields(new_instance):
                cls._instance.__setattr__(
                    field.name, new_instance.__getattribute__(field.name)
                )
        else:
            cls._instance = new_instance

    @classmethod
    def get(cls, *, fallback_to_class: bool = False) -> "Context | type[Context]":
        if not cls._instance:
            if fallback_to_class:
                return Context
            else:
                raise OSError("Uninitialized context")  # pragma: no cover
        return cls._instance

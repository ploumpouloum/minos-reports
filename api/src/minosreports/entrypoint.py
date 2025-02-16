import argparse

from minosreports.constants import (
    NAME,
    VERSION,
)
from minosreports.context import Context


def prepare_context(raw_args: list[str]) -> None:
    """Initialize scraper context from command line arguments"""

    parser = argparse.ArgumentParser(
        prog=NAME,
    )

    parser.add_argument(
        "--version",
        help="Display version and exit",
        action="version",
        version=VERSION,
    )

    parser.add_argument("--debug", help="Enable verbose output", action="store_true")

    args = parser.parse_args(raw_args)

    # Ignore unset values so they do not override the default specified in Context
    args_dict = {key: value for key, value in args._get_kwargs() if value}

    Context.setup(**args_dict)

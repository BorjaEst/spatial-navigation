"""Utility functions and classes for the spnav package."""

# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-arguments

from pydantic_settings import (BaseSettings, CliSettingsSource,
                               PydanticBaseSettingsSource)
from rich.console import Console
from rich_argparse import RichHelpFormatter

console = Console()


class BaseArguments(BaseSettings):
    """Base class for all scripts"""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Enable CLI formatter_class to work properly."""
        return (
            CliSettingsSource(
                settings_cls,
                formatter_class=RichHelpFormatter,
                cli_parse_args=True,
            ),
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )

"""Module for loading and retrieving parameters for configuration and settings."""

from importlib.metadata import version

from application_settings.configuring_base import ConfigBase, ConfigSectionBase, ConfigT
from application_settings.container_section_base import SectionTypeStr
from application_settings.convenience import (
    config_filepath_from_cli,
    parameters_folderpath_from_cli,
    settings_filepath_from_cli,
)
from application_settings.settings_base import (
    SettingsBase,
    SettingsSectionBase,
    SettingsT,
)
from application_settings.type_notation_helper import PathOpt, PathOrStr

__version__ = version("application_settings")

__all__ = [
    "ConfigSectionBase",
    "ConfigBase",
    "ConfigT",
    "PathOpt",
    "PathOrStr",
    "SectionTypeStr",
    "SettingsSectionBase",
    "SettingsBase",
    "SettingsT",
    "config_filepath_from_cli",
    "settings_filepath_from_cli",
    "parameters_folderpath_from_cli",
]

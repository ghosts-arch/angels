# encode : utf-8
# Python 3.10
# ----------------------------------------------------------------------------

import yaml

from typing import TypedDict
from pathlib import Path


class Config(TypedDict):
    CERTIFIED_ROLE: int
    GUILD_ID: int
    TEST_CHANNEL_ID: int
    DEV_MODE: bool
    ADMINSTRATION_CHANNEL_ID: int


def load_config(path: Path) -> Config:
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return validate_config(config)


def validate_config(config: Config) -> Config:
    for key in config.keys():
        if not config[key]:
            raise Exception(f"{key} is not set in config")
    return config

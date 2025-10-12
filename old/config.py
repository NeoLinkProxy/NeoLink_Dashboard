import yaml
import os

from typing import TypedDict, Literal

from folder import folder


class Config(TypedDict):
    Mirror: Literal['https://bgithub.xyz/']
    Site: Literal['https://github.com/']


def GetConfig() -> Config:
    with open(os.path.join(folder, './config.yaml'), "r") as f:
        return yaml.safe_load(f) # pyright: ignore[reportUnknownVariableType]

config = GetConfig()

name = 'NeoLinkProxy'
VersionRepository = 'NeoLinkVersions'
branch = 'main'

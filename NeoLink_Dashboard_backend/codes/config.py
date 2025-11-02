from typing import Literal, TypedDict
# import semantic_version as sv


class NeoLinkProxy:
    name = 'NeoLinkProxy'
    # def __init__(self) -> None:
    #     self.name = 'NeoLinkProxy'

class NeoLinkVersions(NeoLinkProxy):
    name = NeoLinkProxy.name
    Repository = 'NeoLinkVersions'
    branch = 'main'

    files: tuple[
        Literal['Versions.yaml'],
        Literal['VersionsList.yaml'],
        Literal['latest.yaml']
    ] = (
        'Versions.yaml',
        'VersionsList.yaml',
        'latest.yaml',
    )
    # def __init__(self) -> None:
    #     super().__init__()
    #     self.name = super().name
    #     self.Repository = 'NeoLinkVersions'
    #     self.branch = 'main'
    
    #     self.files: tuple[
    #         Literal['Versions.yaml'],
    #         Literal['VersionsList.yaml'],
    #         Literal['latest.yaml']
    #     ] = (
    #         'Versions.yaml',
    #         'VersionsList.yaml',
    #         'latest.yaml',
    #     )

class NeoLinkVersion_Latest(TypedDict):
    jar: str # jar 文件
    exe: str # exe 文件
    config: str # 配置文件
    env: str # 包含环境的文件
    version: str # 版本（Version.yaml里不需要存在）

from Edition_logs import Edition_logs


def GetVersion():
    version = ''

    for _ in Edition_logs.split('\n'):
        if _.endswith(' 版本：'):
            version: str = _[:-4]
        elif _.endswith(' 版本：\r'):
            version: str = _[:-5]
    
    return version

def GetVersion_FromExternal(EditionLogs: str) -> str:
    version = ''

    for _ in EditionLogs.split('\n'):
        if _.endswith(' 版本：'):
            version: str = _[:-4]
        elif _.endswith(' 版本：\r'):
            version: str = _[:-5]
    
    return version

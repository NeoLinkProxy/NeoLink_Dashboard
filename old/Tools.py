import requests


class DevThing:
    def __init__(self, name: str, InDev: bool=False):
        self.InDev = InDev
        self.name = name

    def ChangeInDev(self, newInDev: bool):
        self.InDev = newInDev
        
    def dev_print(
        self,
        *values: object,
        sep: str | None = " ",
        end: str | None = "\n",
        flush: bool = False
    ) -> None:
        return print(f'{self.name} dev :', *values, sep=sep, end=end, flush=flush) if self.InDev else None

def GetContentFromGithub(name: str, rep: str, bra: str, filepath: str, use_china_mirror: bool = False) -> str:
    """
    从GitHub获取文件内容，支持中国内地镜像加速
    
    Args:
        name: 用户名
        rep: 仓库名
        bra: 分支名
        filepath: 文件路径
        use_china_mirror: 是否使用中国镜像加速
    
    Returns:
        文件内容字符串
    """
    # 中国内地常用的GitHub镜像站
    china_mirrors = [
        # f'https://cdn.jsdelivr.net/gh/{name}/{rep}@{bra}/{filepath}',
        f'https://hub.gitmirror.com/'
    ]
    
    # 默认使用原始GitHub链接
    url = f'https://raw.githubusercontent.com/{name}/{rep}/{bra}/{filepath}'

    # 如果指定使用中国镜像，则尝试镜像站点
    if use_china_mirror:
        for mirror_url in china_mirrors:
            try:
                response = requests.get(mirror_url + url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"镜像站点 {mirror_url} 访问失败: {e}")
                continue
    
    # 如果未使用镜像或镜像访问失败，回退到原始URL
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

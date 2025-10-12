# 打开 Powershell ，并执行 cd ./ReStart 和 pnpm run dev
# 打开 Powershell ，并执行 cd ./ReStartGame 和 uv run ReStartGame.py
# 同时执行，并且有 Powershell 的窗口
import subprocess
import os
import pathlib
import sys
from typing import TypeVar


# 获取当前工作目录
# cwd = os.getcwd()
folder = pathlib.Path(__file__).parent.resolve()


T = TypeVar('T')

def get(lst: list[T], index: int, default: T | None = None) -> T | None:
    """安全获取列表元素"""
    try:
        return lst[index]
    except IndexError:
        return default

if not (a:=get(sys.argv, 1)) is None:
    if a == 'build':
        quit()
    else:
        print('无效的参数')
        quit()
else:
    # 构造第一个 PowerShell 命令：进入 ReStart 目录并运行 pnpm dev
    cmd1 = f'cd "{folder}\\PosintGamingPlatform"; pnpm run dev; Read-Host -Prompt "Press Enter to exit"'

    # 构造第二个 PowerShell 命令：进入 ReStartGame 目录并运行 uv run ReStart.py
    cmd2 = f'cd "{folder}\\PosintGamingPlatform_backend"; uv run PosintGamingPlatform.py; Read-Host -Prompt "Press Enter to exit"'

# 启动第一个 PowerShell 窗口
subprocess.Popen(['powershell.exe', '-Command', cmd1])

# 启动第二个 PowerShell 窗口
subprocess.Popen(['powershell.exe', '-Command', cmd2])

# 等待用户输入以保持主程序运行
try:input("Press Enter to close this launcher...")
except KeyboardInterrupt: pass

os._exit(0)

import os
import subprocess
import pathlib


# 获取当前工作目录
# cwd = os.getcwd()
folder = pathlib.Path(__file__).parent.resolve()

psplist: list[subprocess.Popen[str]] = []

# 打开一个可见 Powershell 窗口，而不是在原来的命令行中输出
def open_powershell_window():
    # 使用 subprocess.Popen 创建一个新的 PowerShell 进程
    # powershell.exe 是 PowerShell 的可执行文件
    # -NoExit 参数使 PowerShell 窗口在执行完命令后保持打开状态
    process = subprocess.Popen(
        args=[
            "powershell.exe", 
            # "-NoExit"
        ], 
        stdin=subprocess.PIPE, 
        # stdout=subprocess.PIPE, 
        # stderr=subprocess.PIPE, 
        text=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE  # 创建新的控制台窗口
    )

    psplist.append(process)
    
    return process

# 创建 PowerShell 进程
ps_process1 = open_powershell_window()
ps_process2 = open_powershell_window()

# 示例：向 PowerShell 窗口发送命令
def send_command(process: subprocess.Popen[str], command: str):
    """
    向 PowerShell 进程发送命令
    
    Args:
        process: PowerShell 进程对象
        command (str): 要执行的命令
    Returns:
        None: 正常结束
    Raises:
        RuntimeError: stdin 未初始化。
    """
    # 向 PowerShell 进程的标准输入写入命令
    if process.stdin is not None:
        process.stdin.write(command + "\n")
        process.stdin.flush()
    else:
        raise RuntimeError("无法向 PowerShell 进程写入命令，stdin 未初始化。")
    
def exit_():
    # import time
    # 修复1: 处理所有进程，而不是 len(psplist) - 1 个
    while psplist:  # 使用 while 循环处理所有进程
        psp = psplist.pop(0)
        # 强制停止 psp 正在执行的命令
        try:
            # 尝试终止进程
            psp.terminate()
            # 等待进程结束
            psp.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # 如果进程在5秒内未结束，则强制杀死
            psp.kill()
        except Exception:
            # 忽略其他异常，确保继续处理下一个进程
            pass

send_command(ps_process1, f'cd "{folder}\\NeoLink_Dashboard_frontend"')
send_command(ps_process1, f'pnpm run dev')

send_command(ps_process2, f'cd "{folder}\\NeoLink_Dashboard_backend"')
send_command(ps_process2, f'uv run NeoLink_Dashboard.py')

# 等待用户输入以保持程序运行
input("按 Enter 键退出...")

exit_()

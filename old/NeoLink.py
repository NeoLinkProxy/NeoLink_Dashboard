import tkinter as tk
import tkintertools as tkt # pyright: ignore[reportMissingTypeStubs]
import os
import subprocess
import traceback
import threading

from tkinter import scrolledtext


class NeoLink:
    def __init__(
            self,
            root: tk.Tk | tkt.Tk,
            filePath: str,
            NeoLinkPath: str,
            LocalPort: int,
            SerialNumber: str,
        ):
        self.filePath: str = filePath
        self.NeoLinkPath: str = NeoLinkPath
        self.LocalPort: int = LocalPort
        self.SerialNumber: str = SerialNumber
        self.root: tk.Tk | tkt.Tk = root
        self.parents = tk.Frame(self.root)
        self.parents.pack()

        self.process = None  # 添加进程引用
        self.running = True  # 添加运行状态标志

        self.output = scrolledtext.ScrolledText(self.parents)
        self.output.pack()

        self.Content = ''

        self.copyTextBtn = tk.Button(self.parents, text='复制文本', command=self.copyText)
        self.copyTextBtn.pack()

        self.stopBtn = tk.Button(self.parents, text='关闭', command=self.exit)
        self.stopBtn.pack()

        self.thread = threading.Thread(target=self.RunNeoLink)
        self.thread.start()

        self.root.after(500, self.update)

    def RunNeoLink(self):
        if not os.path.exists(self.filePath):
            with open(self.filePath, 'w', encoding='UTF-8') as f:
                f.write('')
        else:
            with open(self.filePath, 'w', encoding='UTF-8') as f:
                f.write('')

        try:
            # 先切换到工作目录
            os.chdir(os.path.dirname(self.NeoLinkPath))

            # 根据文件类型决定执行方式
            if self.NeoLinkPath.endswith('.jar'):
                # # JAR 文件需要用 Java 执行
                # cmd = [
                #     self.JavaPath, '-jar', self.NeoLinkPath,
                #     '--zh-cn',
                #     f'--key:{self.SerialNumber}',
                #     f'--local-port:{self.LocalPort}',
                #     f'--output-file:{self.filePath}',
                # ]
                
                with open(self.filePath, 'w', encoding='UTF-8') as f:
                    f.write(f'NeoLink 执行出错 (退出码: None)\n')
                    f.write('=' * 50 + '\n')
                    f.write('无法运行 jar 版本！')
                return
            else:
                # 直接执行 exe 文件
                cmd = [
                    self.NeoLinkPath,
                    '--zh-cn',
                    f'--key:{self.SerialNumber}',
                    f'--local-port:{self.LocalPort}',
                    f'--output-file:{self.filePath}',
                ]
            
            # print(f"执行命令: {' '.join(cmd)}")
            
            # 使用 Popen 以便可以控制进程
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 等待进程结束
            stdout, stderr = self.process.communicate()
            
            # 检查进程返回码
            if self.process.returncode != 0 and self.running:
                with open(self.filePath, 'w', encoding='UTF-8') as f:
                    f.write(f'NeoLink 执行出错 (退出码: {self.process.returncode})\n')
                    f.write('=' * 50 + '\n')
                    f.write('标准输出:\n')
                    f.write(stdout if stdout else '无输出\n')
                    f.write('\n' + '=' * 50 + '\n')
                    f.write('错误输出:\n')
                    f.write(stderr if stderr else '无错误信息\n')
                    f.write('\n' + '=' * 50 + '\n')
                    f.write('命令行参数:\n')
                    f.write(' '.join(cmd) + '\n')
            elif self.running:
                # 程序正常执行完成
                pass
                
        except FileNotFoundError as e:
            with open(self.filePath, 'w', encoding='UTF-8') as f:
                f.write(f'文件错误: {str(e)}\n')
                f.write('请检查 NeoLink 路径是否正确\n')
                f.write(traceback.format_exc())
        except Exception as e:
            if self.running:  # 只在仍在运行时记录错误
                with open(self.filePath, 'w', encoding='UTF-8') as f:
                    f.write(f'执行 NeoLink 时出错: {str(e)}\n')
                    f.write(traceback.format_exc())

    def exit(self):
        """优雅地关闭 NeoLink 进程和线程"""
        self.running = False
        
        # 如果有正在运行的进程，尝试终止它
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)  # 等待最多5秒
            except subprocess.TimeoutExpired:
                self.process.kill()  # 强制杀死进程
            except Exception:
                pass
        
        # 取消所有计划的任务
        for after_id in self.root.tk.eval('after info').split():
            try:
                self.root.after_cancel(after_id)
            except Exception:
                pass
        
        # 销毁窗口
        try:
            self.root.destroy()
            
            # os._exit(0)
        except Exception:
            pass

    def copyText(self):
        """
        将当前显示的文本内容复制到系统剪贴板
        """
        # 清空剪贴板
        self.root.clipboard_clear()
        # 将当前文本内容复制到剪贴板
        self.root.clipboard_append(self.Content)
        # 更新剪贴板
        self.root.update()
        
        # 可选：显示一个提示信息
        # 创建一个临时提示标签
        notice = tk.Label(self.parents, text="已复制到剪贴板", bg="lightgreen")
        notice.pack()
        # 2秒后自动移除提示
        self.root.after(2000, lambda: notice.destroy())
    
    def update(self):
        with open(self.filePath, 'r', encoding='UTF-8') as f:
            content = f.read()
        if content != self.Content:
            self.Content = content
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, content)
            self.output.see(tk.END)

        self.root.after(500, self.update)

def CreateNeoLink(filePath: str, NeoLinkPath: str, LocalPort: int, SerialNumber: str):
    root = tkt.Tk(title='NeoLink')

    neolink = NeoLink( # pyright: ignore[reportUnusedVariable]
        root=root,
        filePath=filePath,
        NeoLinkPath=NeoLinkPath,
        LocalPort=LocalPort,
        SerialNumber=SerialNumber,
    )

    root.mainloop()

    os._exit(0)

import tkinter as tk
import tkintertools as tkt # pyright: ignore[reportMissingTypeStubs]
import threading
import requests
import time
import os
import yaml
import sys
import tqdm.tk as tqdm_tk

from typing import Literal, TypedDict
from collections.abc import Callable
from tkinter import messagebox

from folder import folder
from config import config, name, VersionRepository, branch
from Tools import DevThing, GetContentFromGithub
from NeoLink import CreateNeoLink
from Notice import Notice


notice = Notice()
CheckDev = DevThing("CheckDev")
AllDev = DevThing("AllDev")
# CheckDev.ChangeInDev(True)
# AllDev.ChangeInDev(True)

class LaVersionDict(TypedDict):
    jar: str
    exe: str
    config: str
    env: str
    version: str

class VersionDict(TypedDict):
    jar: str
    exe: str
    config: str
    env: str

# 添加缓存机制，避免频繁请求
_last_check_result = None
_last_check_time = 0
ChinaUser = False
CACHE_DURATION = 3600  # 1小时缓存

# 判断是否是打包后的exe运行
if getattr(sys, 'frozen', False):
    # 打包后的exe运行，使用exe所在目录
    base_folder = os.path.dirname(sys.executable)
else:
    # 直接运行Python脚本，使用原base_folder路径
    base_folder = folder

# 定义NeoLinks文件夹路径
neo_links_path = os.path.join(base_folder, 'NeoLinks')

# 确保NeoLinks文件夹存在
if not os.path.exists(neo_links_path):
    os.makedirs(neo_links_path)

class NeoLink_kingda:
    def __init__(self, root: tk.Tk | tkt.Tk):
        self.root = root
        self.parents = tk.Frame(self.root)
        self.parents.pack()

        self.pack()

    def pack(self):
        lbl_1 = tk.Label(self.parents, text='')
        lbl_1.pack()
        
        if ChinaUser:
            lbl_1.config(text='检测到您是中国内地用户，切换到镜像网站')
        else:
            lbl_1.config(text='检测到您不是中国内地用户，切换到原始网站')
        
        self.SerialNumber = tk.Entry(self.parents)
        self.SerialNumber.pack()
        
        # 复选框
        self.DowloadLatestNeoLink = tk.Button(self.parents, text='下载最新版 NeoLink ', command=self.download_latest_NeoLink)
        self.DowloadLatestNeoLink.pack()

        self.DownloadNeoLink = tk.Button(self.parents, text='下载指定版 NeoLink ', command=self.download_NeoLink_Version)
        self.DownloadNeoLink.pack()

        self.RunBtn = tk.Button(self.parents, text='运行 NeoLink ',command=self.run)
        self.RunBtn.pack()

    def download_latest_NeoLink(self):
        version: LaVersionDict = yaml.safe_load(GetContentFromGithub(
            name,
            VersionRepository,
            branch,
            'latest.yaml',
            ChinaUser
        ))

        self.download_NeoLink(version)

    def download_NeoLink_Version(self):
        # 获取版本列表
        VersionList = GetNLVersionsList()

        root_ = tkt.Tk(title='选择 NeoLink 版本')
        root_.config(bg="#2B2B2B")
        
        # 创建主框架
        frame = tk.Frame(root_)
        frame.pack(pady=20)
        
        # 创建标签
        label = tk.Label(frame, text="选择版本:")
        label.pack(pady=5)

        # 创建下拉选框
        version_var = tk.StringVar()
        if VersionList:
            version_var.set(VersionList[0])  # 设置默认值
        
        version_dropdown = tk.OptionMenu(frame, version_var, *VersionList)
        version_dropdown.config(width=20)  # 调整为合理宽度
        version_dropdown.pack(pady=10)
        
        # 创建下载按钮
        def download_selected():
            selected_version = version_var.get()
            if selected_version:
                # 这里可以调用下载逻辑
                messagebox.showinfo("提示", f"开始下载版本: {selected_version}")
                root_.destroy()
                
                version_: VersionDict = yaml.safe_load(GetContentFromGithub(
                    name,
                    VersionRepository,
                    branch,
                    'Versions.yaml',
                    ChinaUser
                ))[selected_version]

                _: LaVersionDict = version_.copy()
                _.update({'version': selected_version})
                version: LaVersionDict = _

                self.download_NeoLink(version)

            else:
                messagebox.showerror("错误", "请选择一个版本")
        
        download_btn = tk.Button(frame, text="下载", command=download_selected)
        download_btn.pack(pady=10)
        
        # 如果没有版本，显示提示
        if not VersionList:
            version_dropdown.config(state='disabled')
            messagebox.showwarning("警告", "暂无可用版本")

    def download_NeoLink(self, version: LaVersionDict):
        # 创建队列用于线程间通信
        from queue import Queue
        progress_queue = Queue()
        
        def down():
            try:
                LatestPath = os.path.join(neo_links_path, version["version"])
                if os.path.exists(LatestPath):
                    # 在主线程中显示错误信息
                    root.destroy()
                    self.root.after(0, lambda: messagebox.showerror("错误", f"版本 {version['version']} 已存在"))
                    return
                
                os.mkdir(LatestPath)

                exePath = os.path.join(LatestPath, f'./NeoLink_{version["version"]}.exe')
                cfgPath = os.path.join(LatestPath, f'./config.cfg')

                def downNLEXE():
                    # 获取文件大小
                    resp = requests.get(UseSite + version['exe'], stream=True, timeout=30)
                    resp.raise_for_status()
                    total_size = int(resp.headers.get('content-length', 0))
                    
                    downloaded = 0
                    with open(exePath, 'wb') as f:
                        for chunk in resp.iter_content(chunk_size=8192):  # 增大chunk_size
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                # 通过队列报告进度
                                progress_queue.put(('exe_progress', downloaded, total_size))
                    
                    # 通知下载完成
                    progress_queue.put(('exe_complete',))

                    downNLCFG()

                def downNLCFG():
                    # 获取文件大小
                    resp = requests.get(UseSite + version['config'], stream=True, timeout=30)
                    resp.raise_for_status()
                    total_size = int(resp.headers.get('content-length', 0))
                    
                    downloaded = 0
                    with open(cfgPath, 'wb') as f:
                        for chunk in resp.iter_content(chunk_size=8192):  # 增大chunk_size
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                # 通过队列报告进度
                                progress_queue.put(('cfg_progress', downloaded, total_size))
                    
                    # 通知下载完成
                    progress_queue.put(('cfg_complete',))
                    progress_queue.put(('all_complete',))

                # 启动下载线程
                threadEXE = threading.Thread(target=downNLEXE)
                threadEXE.daemon = True  # 设置为守护线程
                threadEXE.start()

            except Exception as e:
                # 在主线程中显示错误信息
                print(e)
                self.root.after(0, lambda msg=str(e): messagebox.showerror("错误", f"下载出错: {msg}"))

        root = tkt.Tk()
        textLbl = tk.Label(root, text='下载...')
        textLbl.pack()
        root.update()
        # 启动下载
        down()
        
        # 在主线程中处理进度更新
        def process_progress():
            nonlocal root, textLbl
            try:
                while True:  # 处理队列中的所有消息
                    message = progress_queue.get_nowait()
                    if message[0] == 'exe_progress':
                        downloaded, total = message[1], message[2]
                        # 可以在这里更新exe下载进度显示
                        # print(f"EXE下载进度: {downloaded}/{total}")
                        # if not root.winfo_exists():
                        #     root = tkt.Tk()
                        #     textLbl = tk.Label(root, text='下载...')
                        #     textLbl.pack()
                        textLbl.config(text=f"EXE下载进度: {downloaded}/{total} {downloaded / total * 100:.2f}%")
                        root.update()
                    elif message[0] == 'cfg_progress':
                        downloaded, total = message[1], message[2]
                        # 可以在这里更新配置文件下载进度显示
                        # print(f"配置文件下载进度: {downloaded}/{total}")
                        # if not root.winfo_exists():
                        #     root = tkt.Tk()
                        #     textLbl = tk.Label(root, text='下载...')
                        #     textLbl.pack()
                        textLbl.config(text=f"配置文件下载进度: {downloaded}/{total}")
                        root.update()
                    elif message[0] == 'exe_complete':
                        # print("EXE下载完成")
                        # if not root.winfo_exists():
                        #     root = tkt.Tk()
                        #     textLbl = tk.Label(root, text='下载...')
                        #     textLbl.pack()
                        textLbl.config(text="EXE下载完成")
                        root.update()
                    elif message[0] == 'cfg_complete':
                        # print("配置文件下载完成")
                        # if not root.winfo_exists():
                        #     root = tkt.Tk()
                        #     textLbl = tk.Label(root, text='下载...')
                        #     textLbl.pack()
                        textLbl.config(text="配置文件下载完成")
                        root.update()
                    elif message[0] == 'all_complete':
                        # 在主线程中显示完成信息
                        root.destroy()
                        self.root.after(0, lambda: messagebox.showinfo("完成", "下载完成!"))
                        return
            except:
                pass  # 队列为空
            
            # 继续定期检查进度
            self.root.after(100, process_progress)
        
        # 启动进度处理
        process_progress()


    def run(self):
        # 选择NeoLink版本，版本在./NeoLinks文件夹中，
        NLList: list[NeoLinkListDict] = GetNLList()

        nameList: list[str] = [i['name'] for i in NLList]

        

        pass
        # CreateNeoLink(
        #     os.path.join(base_folder, 'log.txt'),
        #     'G:\\NeoLink-3.2-env-bundled\\NeoLink-3.2-RELEASE.exe',
        #     5173,
        #     'abcd',
        # )

class NeoLinkListDict(TypedDict):
    path: str
    name: str

def GetNLList() -> list[NeoLinkListDict]:
    NLList_ = os.listdir(neo_links_path)
    NLList: list[NeoLinkListDict] = []
    for i in NLList_:
        if not os.path.isfile(os.path.join(neo_links_path, i)):
            continue
        elif os.path.exists(os.path.join(neo_links_path, i, 'config.cfg')):
            NLList.append({'path': os.path.join(neo_links_path, i), 'name': i})
            
    return NLList

def GetNLVersionsList() -> list[str]:
    versions: list[str] = yaml.safe_load(GetContentFromGithub(
        name,
        VersionRepository,
        branch,
        'VersionsList.yaml',
        ChinaUser
    ))

    return versions

def check_china_user(callback: Callable[[bool], None] | None=None):
    """检测用户是否在中国内地（不使用异步）"""
    global _last_check_result, _last_check_time
    
    # 检查缓存
    current_time = time.time()
    if _last_check_result is not None and (current_time - _last_check_time) < CACHE_DURATION:
        CheckDev.dev_print(f"使用缓存的检测结果: {_last_check_result}")
        if callback:
            callback(_last_check_result)
        return
    
    try:
        # 使用多个备选服务提高可靠性
        services = [
            "https://ipapi.co/json/",
            "https://ipwho.is/",
            "http://www.geoplugin.net/json.gp"
        ]
        
        country = ""
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                data = response.json()
                CheckDev.dev_print(f"服务 {service} 返回数据: {data}")
                
                # 根据不同服务的返回格式提取国家代码
                if 'error' in data and data['error']:
                    continue  # 跳过有错误的服务
                
                if 'country' in data:
                    country = data['country']
                elif 'country_code' in data:
                    country = data['country_code']
                elif 'geoplugin_countryCode' in data:
                    country = data['geoplugin_countryCode']
                
                if country:
                    break  # 成功获取到国家代码就退出循环
                    
            except Exception as service_error:
                print(f"服务 {service} 请求失败: {service_error}")
                continue
        
        if not country:
            raise Exception("所有地理位置服务都不可用")
        
        # 判断是否为中国大陆地区
        is_china_user = (country.upper() in ["CN", "CHN", "CHINA"])
        CheckDev.dev_print(f"用户所在国家/地区: {country}, 是否中国内地: {is_china_user}")
        
        # 缓存结果
        _last_check_result = is_china_user
        _last_check_time = time.time()
        
        if callback:
            callback(is_china_user)
            
    except Exception as e:
        CheckDev.dev_print(f"地理位置检测失败: {e}")
        # 出现异常时使用缓存结果或默认不视为中国用户
        if _last_check_result is not None:
            result = _last_check_result
        else:
            result = False  # 默认值
            
        if callback:
            callback(result)

UseSite: Literal['https://bgithub.xyz/', 'https://github.com/'] = config["Site"]

def check_cb(is_china_user: bool):
    global UseSite, ChinaUser
    ChinaUser = is_china_user
    if is_china_user:
        UseSite = config["Mirror"]
    else:
        UseSite = config["Site"]
    AllDev.dev_print(f"{UseSite = }")

def main():
    # print('检测中\n', '正在进行检测，请稍候...', sep='    ')
    notice.EmitNotice_New('检测中', '正在进行检测，请稍候...')
    check_china_user(callback=check_cb)
    AllDev.dev_print(config)
    # threading.Thread(target=lambda: AllDev.dev_print(GetContentFromGithub(name, repository, branch, 'latest.yaml', ChinaUser))).start()

    root = tkt.Tk(title="NeoLink Kingda")
    root.config(bg="#2B2B2B")
    app = NeoLink_kingda(root=root)

    root.mainloop()

if __name__ == "__main__":
    main()

from collections.abc import Callable
import shutil
import flask
from flask_cors import CORS
from typing import Literal, TypedDict
from threading import Thread
import os
import webview # pyright: ignore[reportUnusedImport]
import yaml
# import shutil
import multiprocessing
# import json
import time
from pathlib import Path
import requests
from tkinter import filedialog
import subprocess
from .Notice import Notice
from .Edition_logs import Edition_logs
from .folder import folder
from .versions import GetVersion
from .VersionSystem import VersionSystem
# from PIL import Image
# from Scenario import Scenario, ScenarioDict
# import traceback
import platform
from uuid import uuid4
import semantic_version as sv # pyright: ignore[reportMissingTypeStubs]
import webbrowser
from .config import NeoLinkVersions, NeoLinkVersion_Latest
from .Tools import DevThing, GetContentFromGithub
import SV_CanNoPatch # pyright: ignore[reportMissingTypeStubs]
from .TrafficForwarder import create_TrafficFowarder


_NLK_process = None
_NLK_window = None
IsChinaUser: bool = False


notice = Notice()

version = GetVersion()

class popupDict(TypedDict):
    title: str
    message: str
    type: Literal['info', 'warning', 'error']


class ErrorDict(TypedDict):
    message: str
    stack: str
    name: str
    timestamp: str

class VersionDict(TypedDict):
    jar: str # jar 文件
    exe: str # exe 文件
    config: str # 配置文件
    env: str # 包含环境的文件


def get_dataDir_path() -> str:
    """获取数据目录路径"""
    # 修改为跨平台兼容的用户目录获取方式
    if platform.system() == "Windows":
        username = os.getenv('USERNAME')
        gamelist_dir = f'C:/Users/{username}/.NeoLink_Dashboard/'
    elif platform.system() == "Darwin":  # macOS
        username = os.getenv('USER')
        gamelist_dir = f'/Users/{username}/.NeoLink_Dashboard/'
    else:  # Linux 和其他类Unix系统
        username = os.getenv('USER')
        gamelist_dir = f'/home/{username}/.NeoLink_Dashboard/'
    
    # 确保目录存在
    Path(gamelist_dir).mkdir(parents=True, exist_ok=True)

    return gamelist_dir

def API_section() -> None:
    app_API = flask.Flask('NLD_API')
    CORS(app_API)  # 启用 CORS 支持S
    app_API.config["DEBUG"] = False

    # 上报错误
    @app_API.route('/error', methods=['POST'])
    def report_error() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        error: ErrorDict = flask.request.json # pyright: ignore[reportAssignmentType]
        error_path = os.path.join(get_dataDir_path(), 'error.log')
        with open(error_path, 'a', encoding='utf-8') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}-Start\n{error['name']}: {error['message']}\n{error['stack']}\non {error['timestamp']}\nEnd\n")
        return flask.jsonify({'message': '错误已上报'})

    # 获取当前的版本
    @app_API.route('/version', methods=['GET'])
    def get_version() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        return flask.jsonify({
            'version': version
        })
    
    @app_API.route('/save/Setting/NeoLinkDownloadPath/', methods=['POST'])
    def save_NeoLinkDownloadPath() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        path: str | None = flask.request.json['path'] # pyright: ignore[reportUnknownVariableType, reportOptionalSubscript, reportAssignmentType]
        type_: Literal['default', 'data', 'custom'] = flask.request.json['type_'] # pyright: ignore[reportUnknownVariableType, reportOptionalSubscript, reportAssignmentType]
        Setting_path = os.path.join(get_dataDir_path(), './Setting/Path.yaml')
        if type_ not in ['default', 'data', 'custom']:
            rep = flask.jsonify({
                'msg': 'type_ 必须是 default, data, custom 中的一个'
            })
            rep.status_code = 1005
            return rep
        if (type_ == 'default' or type_ == 'data') and path is not None:
            rep = flask.jsonify({
                'msg': '当 type_ 为 default 或 data 类型不可指定路径'
            })
            rep.status_code = 1005
            return rep
        
        setting = {
            'type_': type_,
            'path': path
        }
        with open(Setting_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(setting, f, allow_unicode=True)
        return flask.jsonify({'msg': '路径设置已保存'})

    # 获取当前使用的NeoLink的名字
    @app_API.route('/GetNowUseNLV/', methods=['GET'])
    def get_NeoLink_version() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        return flask.jsonify({
            'version': 'None'
        })

    # 获取支持的NeoLink版本
    @app_API.route('/GetSupportedVersions/', methods=['GET'])
    def get_supported_NeoLink_versions() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        list_: list[str] = yaml.safe_load(GetContentFromGithub(
            NeoLinkVersions.name,
            NeoLinkVersions.Repository,
            NeoLinkVersions.branch,
            NeoLinkVersions.files[1],
            use_china_mirror=IsChinaUser,
        ))
        # Versions = yaml.safe_load(GetContentFromGithub(
        #     NeoLinkVersions.name,
        #     NeoLinkVersions.Repository,
        #     NeoLinkVersions.branch,
        #     NeoLinkVersions.files[0],
        #     use_china_mirror=IsChinaUser,
        # ))
        return flask.jsonify({
            'VersionsList': list_,
            # 'Versions': Versions
        })

    # 下载指定的NeoLink版本
    @app_API.route('/DownloadNeoLink/', methods=['POST'])
    def download_NeoLink() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        version: str = flask.request.json['version'] # pyright: ignore[reportUnknownVariableType, reportOptionalSubscript, reportAssignmentType]
        name: str = flask.request.json['name'] # pyright: ignore[reportUnknownVariableType, reportOptionalSubscript, reportAssignmentType]

        Versions: dict[str, VersionDict] = yaml.safe_load(GetContentFromGithub(
            NeoLinkVersions.name,
            NeoLinkVersions.Repository,
            NeoLinkVersions.branch,
            NeoLinkVersions.files[0],
            use_china_mirror=IsChinaUser,
        ))
        # Versions = yaml.safe_load(GetContentFromGithub(
        #     NeoLinkVersions.name,
        #     NeoLinkVersions.Repository,
        #     NeoLinkVersions.branch,
        #     NeoLinkVersions.files[0],
        #     use_china_mirror=IsChinaUser,
        # ))
        if type(version) != str: # pyright: ignore[reportUnknownArgumentType]
            rep = flask.jsonify({
                'msg': 'NeoLink版本不是字符串'
            })
            rep.status_code = 1004
            return rep
        if type(name) != str: # pyright: ignore[reportUnknownArgumentType]
            rep = flask.jsonify({
                'msg': 'NeoLink名字不是字符串'
            })
            rep.status_code = 1004
            return rep

        if version in Versions.keys():
            Version: VersionDict = Versions[version]
            print(Version)
        else:
            rep = flask.jsonify({
                'msg': 'NeoLink版本不在NeoLink版本中'
            })
            rep.status_code = 1003
            return rep

        return flask.jsonify({
            # 'VersionsList': list_,
            # 'Versions': Versions
        })
    
    # 运行 NeoLink （指定的名字）
    @app_API.route('/RunNeoLink/', methods=['POST'])
    def run_NeoLink() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        name: str = flask.request.json['name'] # pyright: ignore[reportUnknownVariableType, reportOptionalSubscript, reportAssignmentType]

        Versions: dict[str, VersionDict] = yaml.safe_load(GetContentFromGithub(
            NeoLinkVersions.name,
            NeoLinkVersions.Repository,
            NeoLinkVersions.branch,
            NeoLinkVersions.files[0],
            use_china_mirror=IsChinaUser,
        ))
        # Versions = yaml.safe_load(GetContentFromGithub(
        #     NeoLinkVersions.name,
        #     NeoLinkVersions.Repository,
        #     NeoLinkVersions.branch,
        #     NeoLinkVersions.files[0],
        #     use_china_mirror=IsChinaUser,
        # ))
        if type(name) != str: # pyright: ignore[reportUnknownArgumentType]
            rep = flask.jsonify({
                'msg': 'NeoLink名字不是字符串'
            })
            rep.status_code = 1004
            return rep

        if name in Versions.keys():
            Version: VersionDict = Versions[name]
            print(Version)
        else:
            rep = flask.jsonify({
                'msg': 'NeoLink名字不在NeoLink版本中'
            })
            rep.status_code = 1003
            return rep

        return flask.jsonify({
            # 'VersionsList': list_,
            # 'Versions': Versions
        })

    # 显示 弹窗
    @app_API.route('/show/popup', methods=['POST'])
    def show_popup() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        popup: popupDict = flask.request.json # pyright: ignore[reportAssignmentType]
        
        if popup['type'] == 'info':
            notice.EmitNotice_New(popup['title'], popup['message'])
        elif popup['type'] == 'warning':
            notice.EmitWarningNotice_New(popup['title'], popup['message'])
        elif popup['type'] == 'error':
            notice.EmitErrorNotice_New(popup['title'], popup['message'])
        
        return flask.jsonify({
            'message': '成功发送弹窗'
        })

    @app_API.route('/Edition_logs', methods=['GET'])
    def get_Edition_logs() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        return flask.jsonify({
            'Edition_logs': Edition_logs
        })
    
    @app_API.route('/Get_is_china_user', methods=['GET'])
    def get_is_china_user() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        """获取用户是否在中国内地"""
        return flask.jsonify({
            'IsChinaUser': IsChinaUser
        })

    @app_API.route('/check_china_user', methods=['GET'])
    def check_china_user(): # pyright: ignore[reportUnusedFunction]
        """检测用户是否在中国内地（不使用异步）"""
        global IsChinaUser
        try:
            # 使用多个备选服务提高可靠性
            services = ["https://ipwho.is/"]
            
            country = ""
            for service in services:
                try:
                    response = requests.get(service, timeout=5)
                    data = response.json()
                    
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

            IsChinaUser = is_china_user
            
        except Exception as e:
            IsChinaUser = False
            # print('a')
            res = flask.jsonify({
                'error': str(e),
                'ischinauser': False
            })
            res.status_code = 500
            return res
        
        return flask.jsonify({
            'ischinauser': is_china_user
        })

    app_API.run(port=23104, debug=False)

def main_section():
    # 在子线程中启动 API 部分
    api_thread = Thread(target=API_section)
    api_thread.daemon = True  # 设置为守护线程，主程序退出时自动退出
    api_thread.start()

    app = flask.Flask('NLD')
    CORS(app)  # 启用 CORS 支持
    app.config["DEBUG"] = False

    @app.route('/', methods=['GET'])
    def home() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        # 返回 index.html
        return flask.send_from_directory(os.path.join(folder, '../files/'), 'index.html')

    # 添加一个通用的静态文件路由来处理所有文件
    @app.route('/<path:filename>')
    # @app.route('/<path:filename>/')
    def static_files(filename: str) -> flask.Response: # pyright: ignore[reportUnusedFunction]
        # print(os.path.join(folder, './files/', filename + '/index.html'))
        path = os.path.join(folder, '../files/', filename)
        if os.path.exists(path) and os.path.isfile(path):
            print('1')
            return flask.send_file(path)
        elif os.path.isdir(path):
            print('2')
            return flask.send_from_directory(os.path.join(folder, './files/'), 'index.html')
        else:
            print('3')
            return flask.abort(404)
    
    @app.route('/assets/<path:filename>')
    def assets_files(filename: str) -> flask.Response: # pyright: ignore[reportUnusedFunction]
        """处理 assets 目录下的文件"""
        file_path = os.path.join(folder, '../files/assets/', filename)
        if os.path.exists(file_path):
            return flask.send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))
        else:
            return flask.abort(404)

    app.run(port=23004, debug=False)

def StartGP():
    try:
        main_thread = Thread(target=main_section)
        main_thread.daemon = True  # 设置为守护线程，主程序退出时自动退出
        main_thread.start()

        class Api:
            def open_url(self, url: str):
                webbrowser.open(url)

        # 在创建webview窗口时注册API
        api = Api()

        global _NLK_window
        _NLK_window = webview.create_window('NeoLink 仪表盘 NeoLink Dashboard', 'http://localhost:23004/', width=800, height=600, js_api=api)
        
        webview.start()
        # try:
        #     while True:
        #         pass
        # except KeyboardInterrupt:
        #     pass

        return False  # 表示正常退出
    except KeyboardInterrupt:
        return False

def run_GP():
    """运行进程"""
    StartGP()

def main():
    global _NLK_process
    
    if multiprocessing.current_process() != 'MainProcess': # pyright: ignore[reportUnnecessaryComparison]
        run_GP()
    else:
        try:
            while True:
                # 启动进程
                _NLK_process = multiprocessing.Process(target=run_GP)
                _NLK_process.start()
                
                # 等待进程结束
                _NLK_process.join()
                
                # 检查退出码，如果不是1则表示正常退出
                if _NLK_process.exitcode != 1:
                    break
        except KeyboardInterrupt:
            os._exit(0)

if __name__ == "__main__":
    main()
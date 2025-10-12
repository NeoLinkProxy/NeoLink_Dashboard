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
from Notice import Notice
from Edition_logs import Edition_logs
from folder import folder
from versions import GetVersion
from VersionSystem import VersionSystem
# from PIL import Image
# from Scenario import Scenario, ScenarioDict
# import traceback
import platform
from uuid import uuid4
import semantic_version as sv # pyright: ignore[reportMissingTypeStubs]


_NLK_process = None
_NLK_window = None


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
    app_API = flask.Flask('PGP_API')
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
    
    # 获取当前使用的NeoLink的名字
    @app_API.route('/GetNowUseNLV/', methods=['GET'])
    def get_NeoLink_version() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        return flask.jsonify({
            'version': 'None'
        })

    # 获取支持的NeoLink版本
    @app_API.route('/GetSupportedVersions/', methods=['GET'])
    def get_supported_NeoLink_versions() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        return flask.jsonify({
            'versions': ['a', 'b']
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
    
    app_API.run(port=23104, debug=False)

def main_section():
    # 在子线程中启动 API 部分
    api_thread = Thread(target=API_section)
    api_thread.daemon = True  # 设置为守护线程，主程序退出时自动退出
    api_thread.start()

    app = flask.Flask('PGP')
    CORS(app)  # 启用 CORS 支持
    app.config["DEBUG"] = False

    @app.route('/', methods=['GET'])
    def home() -> flask.Response: # pyright: ignore[reportUnusedFunction]
        # 返回 index.html
        return flask.send_from_directory(os.path.join(folder, './files/'), 'index.html')

    # 添加一个通用的静态文件路由来处理所有文件
    @app.route('/<path:filename>')
    def static_files(filename: str) -> flask.Response: # pyright: ignore[reportUnusedFunction]
        if os.path.exists(os.path.join(folder, './files/', filename)):
            return flask.send_from_directory(os.path.join(folder, './files/'), filename)
        else:
            return flask.abort(404)
        
    app.run(port=23004, debug=False)

def StartGP():
    try:
        main_thread = Thread(target=main_section)
        main_thread.daemon = True  # 设置为守护线程，主程序退出时自动退出
        main_thread.start()

        global _NLK_window
        _NLK_window = webview.create_window('NeoLink 仪表盘 NeoLink Dashboard', 'http://localhost:23004/', width=800, height=600)
        
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
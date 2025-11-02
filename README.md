# NeoLink 仪表盘 NeoLink Dashboard

> **NeoLink 客户端仪表盘（GUI 版 NeoLink 与 管理器）** 
> 使用 Python 3.13 与 Vue 3.5 开发，支持 NeoLink 4.7.1 及以上版本。

![Python 3.13](https://img.shields.io/badge/Python-3.13-orange?logo=python&logoColor=white)
![Vue 3.5](https://img.shields.io/badge/Vue-3.5-green?logo=vue.js&logoColor=white)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](#许可证)
![Status](https://img.shields.io/badge/Status-Stable-success?logo=github)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red)
---

## 简介

NeoLink Dashboard 是一个现代化的 NeoLink 客户端管理器和图形用户界面，为用户提供直观、便捷的方式来管理和运行 NeoLink 应用。

该仪表盘支持 NeoLink 4.7.1 及以上版本，让用户能够轻松管理多个 NeoLink 实例。

## 功能特性

- 🖥️ 现代化图形用户界面 (GUI)
- 📦 NeoLink 版本管理与切换
- ⚙️ 直观的设置和配置管理
- 📥 在线下载和自动更新功能
- 📋 用户协议和免责声明展示
- 🎨 美观且响应式的 UI 设计

## 项目结构

```
NeoLink_Dashboard/
├── NeoLink_Dashboard_backend/     # 后端代码
│   └── NeoLink_Dashboard.py       # 主程序入口
├── NeoLink_Dashboard_frontend/    # 前端源代码
├── aaa.py                         # 开发环境入口
└── old/                           # 旧版 NeoLink GUI 版（ NeoLink Kingda ） 实现 （已不在使用）
```

## 技术栈

### 后端
- Python 3.13
- Flask (用于本地 API 服务)
- PyWebView (用于嵌入 Web 界面)
- PyGame (用于图形处理)
- Pillow (图像处理)
- Requests (HTTP 请求)
- PyYAML (配置文件处理)
- 其他依赖库 (详见 [pyproject.toml](NeoLink_Dashboard_backend/pyproject.toml))

### 前端
- Vue 3.5
- Vue Router 4.5
- TypeScript 5.8
- Vite 7.0 (构建工具)
- Marked 16.4 (Markdown 解析)
- 其他依赖 (详见 [package.json](NeoLink_Dashboard_frontend/package.json))

## 安装和运行

### 开发环境要求
- Python 3.13+
- Node.js 20.19.0+ 或 22.12.0+ (开发前端时需要)
- pnpm (前端包管理器)

### 开发环境搭建

1. 克隆项目:
   ```bash
   git clone https://github.com/NeoLinkProxy/NeoLink_Dashboard.git
   cd NeoLink_Dashboard
   ```

2. 安装后端依赖:
   ```bash
   cd NeoLink_Dashboard_backend
   pip install -e .
   ```

3. 安装前端依赖:
   ```bash
   cd ../NeoLink_Dashboard_frontend
   pnpm install
   ```

### 开发

1. 使用 uv 同步后端依赖:
   ```bash
   cd NeoLink_Dashboard_backend
   uv sync
   ```

2. 启动开发服务器:
   ```bash
   python aaa.py
   ```

### 构建项目

1. 构建前端:
   ```bash
   cd NeoLink_Dashboard_frontend
   pnpm build
   ```

2. 将生成的 dist 目录下文件复制到后端的 files 目录中

3. 构建后端可执行文件（确保已使用 uv 同步依赖）:
   ```bash
   cd NeoLink_Dashboard_backend
   python build.py
   ```

### 官方发行版

[下载 NeoLink Dashboard 官方发行版](https://github.com/NeoLinkProxy/NeoLink_Dashboard/releases)

### 注意事项

- 建议在生产环境中使用官方提供的 exe 文件，而不是自行编译。

## 使用说明

NeoLink Dashboard 提供了一个直观的用户界面来管理您的 NeoLink 安装。主要功能模块包括：

- **主页**: 显示当前使用的 NeoLink 版本和系统信息
- **下载**: 获取和管理不同版本的 NeoLink
- **设置**: 配置 NeoLink 和仪表盘的各项选项
- **更多**: 查看额外功能和相关信息

## 许可证

本项目基于 [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) 开源发布。

## 支持版本

本仪表盘支持 NeoLink 4.7.1 及以上版本。由于 NeoLink 的差异，不支持更早的版本。

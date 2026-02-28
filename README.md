# 🐧 Python Shell Learner

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**Python Shell Learner** 是一个基于 Python 的命令行游戏，旨在通过沉浸式的终端模拟环境，帮助用户轻松掌握 Linux 常用命令和 Shell 编程技巧。从基础的文件操作到高级的系统运维，60+ 个精心设计的关卡带你一步步成为 Linux 高手！

## ✨ 特性

- **沉浸式体验**：模拟真实的终端环境，支持颜色高亮和命令反馈。
- **渐进式学习**：由浅入深的 5 大阶段，覆盖 60+ 个常用命令。
- **多种模式**：
  - **剧情模式**：按顺序挑战关卡，自动保存进度。
  - **选关模式**：自由练习已解锁或特定的关卡。
  - **随机挑战**：随机抽取关卡，测试你的应变能力。
- **实时反馈**：模拟命令执行结果，提供错误提示和 `hint` 帮助系统。
- **数据持久化**：自动保存游戏进度和得分 (`progress.json`)。

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本

### 安装与运行

1. 克隆仓库或下载源码：

    ```bash
    git clone https://github.com/yeyixiang2007/python-shell-learner.git
    cd python-shell-learner
    ```

2. 运行游戏：

    ```bash
    python main.py
    ```

## 🎮 游戏玩法

游戏启动后，你将看到一个主菜单。选择 **"1. 开始/继续游戏"** 即可进入挑战。

在每个关卡中，你需要在模拟终端中输入正确的 Linux 命令来完成任务。

- **任务目标**：屏幕上方会显示当前关卡的任务描述和初始环境。
- **输入命令**：在 `user@linux-game:path$` 提示符后输入命令并回车。
- **获取帮助**：
  - 输入 `hint`：获取当前关卡的解题提示。
  - 输入 `help`：查看游戏帮助信息。
  - 输入 `exit` 或 `quit`：退出当前挑战或游戏。

## 📚 关卡阶段

游戏共包含 60 个关卡，分为 5 个阶段：

1. **新手入门 (Level 1-17)**
    - 基础文件操作：`ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`
    - 文件查看与权限：`cat`, `chmod`

2. **Shell 编程基础 (Level 18-30)**
    - 变量与环境：`export`, `env`
    - 流程控制：`if`, `for`, `while`
    - 函数与脚本执行

3. **进阶文本与数据处理 (Level 31-37)**
    - 文本处理神器：`sed`, `awk`, `grep`
    - 格式化与转换：`jq`, `iconv`, `fmt`, `split`

4. **网络大师 (Level 38-45)**
    - 下载与传输：`wget`, `curl`, `scp`, `rsync`
    - 网络诊断与分析：`ping`, `netstat`, `tcpdump`, `nslookup`

5. **系统运维 (Level 46-60)**
    - 用户与进程管理：`useradd`, `kill`, `top`, `ps`
    - 磁盘与服务管理：`fdisk`, `mount`, `systemctl`, `journalctl`

## 🛠️ 项目结构

- `main.py`: 游戏入口，负责主菜单和程序启动。
- `engine.py`: 游戏核心引擎，处理命令解析、模拟执行和进度管理。
- `data.py`: 关卡数据文件，定义了所有挑战的任务、预期命令和知识点。
- `utils.py`: 工具函数库，提供颜色输出和界面辅助功能。
- `progress.json`: 自动生成的进度存档文件（请勿手动修改）。

## 📝 贡献

欢迎提交 Issue 或 Pull Request 来改进游戏体验或添加新的关卡！

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

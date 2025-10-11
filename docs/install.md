# 安装指南 / Installation Guide

本页面详细介绍了如何配置运行本项目所需的开发环境、安装依赖、启动服务等步骤。

---

## 1. 下载一些必要的软件 / Download necessary software


<details>
<summary><strong>🧱 Visual Studio 安装与组件配置 (C++环境，UE需要)</strong></summary>

参考配置链接：[为虚幻引擎C++项目设置Visual Studio开发环境](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine?application_version=5.3)

<aside>
💡下载 Visual Studio 2022 Community 版
</aside>

下载地址：[Visual Studio 2022 Community 版](https://visualstudio.microsoft.com/zh-hans/vs/community/)

选择Community即可

![image.png](/assets/image1.png)

在安装设置里面选择安装路径

![image.png](/assets/image2.png)

工作负荷中，勾选这些必要的组件，一共四个

![image.png](/assets/image3.png)

其中`使用C++的桌面开发`的安装详细信息这里，要选择Windows 11 SDK

![image.png](/assets/image4.png)

在单个组件中，搜索`unreal`，然后把所有的都勾选上。因为VS下载的目的就是用在UE上

![image.png](/assets/image5.png)

如果在使用过程中报错，可能是MSVC的错误，就把MSVC换成如下的

![image.png](/assets/image6.png)
</details>

---

<details>
<summary><strong>🐍 CUDA 安装</strong></summary>

<aside>
💡安装CUDA，本次安装CUDA12.6
</aside>

这是下载地址：[CUDA Toolkit 12.6 Downloads](https://developer.nvidia.com/cuda-12-6-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local)

配置版本，然后点击下载就行

![image.png](/assets/image8.png)

</details>

---


<details>
<summary><strong>🎮 安装虚幻引擎 Unreal Engine</strong></summary>


以下是 Unreal Engine 5.3.2 的安装流程，适用于本项目中涉及的 3D 渲染模块。


### 1️⃣ 下载 Epic Games Launcher（启动器）

访问官网并下载安装 Epic Games Launcher：

🔗 [Unreal Engine 5.3.2 下载地址](https://www.unrealengine.com/zh-CN/download)

> Epic Games Launcher 是用于管理和安装 Unreal Engine 的官方启动程序。

![Epic Launcher 下载页面](/assets/image9.png)

---

### 2️⃣ 安装并登录账户

完成安装后，运行 Epic Games Launcher，按照提示创建并登录账户。

![安装步骤](/assets/image10.png)

---

### 3️⃣ 安装 Unreal Engine 5.3.2

登录成功后，进入左侧的 **“虚幻引擎”** 标签页，点击 “安装引擎”。

> 💡 **建议安装在非系统盘（如 D 盘）**，以避免 C 盘空间紧张和后续编译问题。

![选择引擎版本](/assets/image12.png)

选择版本为 **5.3.2** 进行安装：

![安装 UE5.3.2](/assets/image13.png)
</details>

---


<details>
<summary>
<strong>📱 安卓编译环境安装</strong></summary>
首先安装sdk、jdk、ndk、Android Studio

### 1️⃣ 下载并设置安卓依赖环境的路径

![路径设置](/assets/image14.png)

</details> 

---

## 2. 本机部署AI服务

<details>
<summary><strong>🎤 部署ASR (语音识别服务)</strong></summary>

### 项目介绍

**FunASR** 是阿里巴巴达摩院开源的语音识别工具包，提供高性能的语音转文字服务。

🔗 **官方仓库**: [FunASR Github](https://github.com/modelscope/FunASR)  
🔗 **一键部署仓库**: [修改版部署脚本](https://github.com/1m1ng/FunASR)  
📦 **完整环境包**: [FunASR Releases](https://github.com/1m1ng/FunASR/releases)

### 安装步骤

#### 方式一：源码编译安装

1. **编译FunASR服务**
   - 参考 [官方WebSocket教程](https://github.com/modelscope/FunASR/blob/main/runtime/websocket/readme.md) 编译FunASR
   - 将编译后的可执行文件和动态链接库（DLL）放入 `bin` 目录

2. **启动服务**
   - 运行 `run_server_2pass.bat` 脚本
   - 脚本将自动创建Python虚拟环境、安装依赖项并启动FunASR服务器

#### 方式二：一键安装（推荐）

如果编译环境配置有困难，可直接使用预编译的完整环境包：

📥 **下载地址**: [FunASR完整环境包](https://github.com/1m1ng/FunASR/releases)

> 💡 **提示**: 完整环境包包含所有必需的依赖和预训练模型，开箱即用。

</details>

---

<details>
<summary><strong>🚧 部署MeloTTS (语音合成服务)</strong></summary>

### 项目介绍

**MeloTTS** 是MyShell.ai开源的多语言语音合成工具，支持高质量的文字转语音功能。

🔗 **官方仓库**: [MeloTTS Github](https://github.com/myshell-ai/MeloTTS.git)  
🔗 **一键部署仓库**: [修改版部署脚本](https://github.com/1m1ng/MeloTTS)  
📦 **完整环境包**: [MeloTTS Releases](https://github.com/1m1ng/MeloTTS/releases)

### 安装步骤

#### 方式一：源码安装

1. **克隆仓库并安装环境**
   ```bash
   git clone https://github.com/1m1ng/MeloTTS.git
   cd MeloTTS
   ```

2. **首次环境配置**
   - 运行 `install.bat` 安装Python环境和依赖项

3. **模型配置**
   - 将训练好的语音模型权重文件放入 `Weight` 目录
   - 编辑 `config.yaml` 配置文件，确保以下路径正确：
     - `config_path`: 模型配置文件路径
     - `ckpt_path`: 模型权重文件路径

4. **启动服务**
   - 运行 `start.bat` 启动FastAPI服务器

#### 方式二：一键安装（推荐）

如果环境配置遇到问题，建议使用预配置的完整环境包：

📥 **下载地址**: [MeloTTS完整环境包](https://github.com/1m1ng/MeloTTS/releases)

> 💡 **提示**: 完整环境包包含测试用的预训练模型，可直接启动服务进行测试。

</details>

---

<details>
<summary><strong>🚧 部署GPT-SoVITS (语音合成服务)</strong></summary>

### 项目介绍

**GPT-SoVITS** 是由RVC-Boss团队开源的强大语音合成工具，采用GPT架构结合SoVITS技术，支持少样本语音克隆和高质量语音合成。

🔗 **官方仓库**: [GPT-SoVITS Github](https://github.com/RVC-Boss/GPT-SoVITS.git)  
📖 **官方文档**: [中文安装指南](https://github.com/RVC-Boss/GPT-SoVITS/blob/main/docs/cn/README.md)  
📚 **训练教程**: [GPT-SoVITS训练指南](https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e)

### 安装步骤

#### 方式一：源码安装

1. **克隆仓库**
   ```bash
   git clone https://github.com/RVC-Boss/GPT-SoVITS.git
   cd GPT-SoVITS
   ```

2. **环境配置**
   - 安装Python 3.9+ 环境
   - 安装CUDA（推荐CUDA 11.8+）
   - 运行环境安装脚本：
     ```bash
     pip install -r requirements.txt
     ```

3. **模型下载**
   - 下载预训练基础模型
   - 根据需求下载对应语言的预训练权重

4. **模型训练（可选）**
   - 准备训练数据（音频文件 + 对应文本标注）
   - 参考 [GPT-SoVITS训练指南](https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e) 进行模型训练
   - 训练完成后将模型权重放入指定目录

5. **启动WebAPI服务**
   ```bash
   python api_v2.py
   ```
   - 详细配置参数请参考 [api_v2.py](https://github.com/RVC-Boss/GPT-SoVITS/blob/main/api_v2.py) 文件中的文档

#### 方式二：整合包安装（推荐新手）

如果对环境配置不熟悉，建议寻找社区提供的整合包或Docker镜像

> 💡 **提示**: GPT-SoVITS对硬件要求较高，建议使用具备4GB+显存的NVIDIA显卡，CPU推理速度较慢。

</details>

---

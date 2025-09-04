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


<details> <summary><strong>🎮 安装虚幻引擎 Unreal Engine</strong></summary>



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

<p align="center">
  <img src="/assets/image11.png" alt="Epic 登录示意" style="width:15%;"/>
</p>

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
 <summary><strong>💡 下载Audio2Face  </strong></summary>


<font color="red">注：由于audio2face在下载依赖时需访问谷歌服务器导致下载速度极慢，且对显存资源占用极高，尽管其嘴型驱动效果优于ovrlipsync，若可接受ovrlipsync的效果，我们仍推荐优先选用ovrlipsync以规避资源消耗与下载问题。</font>

本指南将帮助你安装 NVIDIA Omniverse Audio2Face（2023.1.1）并导入驱动人脸的模型。包括官网下载安装方式和网盘便捷安装方式。


## 🚀 安装方式一：通过 Omniverse 官网下载安装

### 1️⃣ 下载 Omniverse Launcher

你可以从 NVIDIA 官网下载安装 Omniverse Launcher（它相当于是一个模块下载器）。

🔗 [官方下载地址](https://developer.nvidia.cn/omniverse?sortBy=developer_learning_library%2Fsort%2Ffeatured_in.omniverse%3Adesc%2Ctitle%3Aasc&hitsPerPage=6#section-%E5%BC%80%E5%A7%8B%E4%BD%BF%E7%94%A8)

![Omniverse Launcher 下载](/assets/image14.png)

---

### 2️⃣ 注册并登录 NVIDIA 账户

完成下载后，注册并登录 NVIDIA 账户。

![登录界面](/assets/image15.png)

---

### 3️⃣ 安装 Audio2Face 2023.1.1

在 Launcher 内搜索并安装 **Audio2Face 2023.1.1**。

![搜索 Audio2Face](/assets/image16.png)
![确认安装](/assets/image17.png)

> 💡 安装过程可能较慢，建议连接稳定网络，部分公司网络可能受限，建议使用手机热点。


---

### 4️⃣ 启动 Audio2Face

完成安装后，点击启动：

![启动界面](/assets/image18.png)

---

### 5️⃣ 导入三维人脸模型（`text.usd`）

从百度网盘下载以下模型文件：

🔗 链接：[百度网盘 text.usd](https://pan.baidu.com/s/1VtY0QrJz285kXtXhJ-rVog?pwd=e9w2)  
提取码：`e9w2`

将 `text.usd` 文件放入 Audio2Face 的工程目录中，打开 Audio2Face 后进入 **Example** 界面，定位到模型目录并双击导入。

![导入 text.usd](/assets/image19.png)

---



### 6️⃣ 成功启动后的界面

反复尝试导入模型，直到看到蓝色人脸即表示加载成功。

![加载成功示意](/assets/image21.png)

⚠️ 初次加载常见问题较多，可通过更换网络、多次重启尝试解决。

![可能遇到的加载错误](/assets/image22.png)

---

### 7️⃣ 解决常见网络问题

如果导入失败，多半是网络问题导致资源加载失败。建议：

- 多尝试，检查网络问题（更换网络环境）

## 🎁 安装方式二：一键安装（网盘便捷方式）

更推荐使用该方式，跳过下载 Launcher 和组件配置的繁琐过程。

### 1️⃣ 下载完整安装包

🔗 链接：[audio2face-2023.1.1.rar 百度网盘](https://pan.baidu.com/s/1fzZNYsHlLC1HUVol2z44ZA?pwd=j7uu)  
提取码：`j7uu`

---

### 2️⃣ 启动程序

解压后，双击 `audio2face.bat` 启动 Audio2Face。

![启动 .bat 脚本](/assets/image23.png)

---

### 3️⃣ 正确启动后的控制台窗口

![控制台窗口](/assets/image24.png)

---

### 4️⃣ 界面加载成功，导入 `text.usd`

不要忘了仍需导入人脸模型 `text.usd`！

![最终成功界面](/assets/image21.png)

## ✅ 补充说明

- 蓝色人脸是 Audio2Face 的默认驱动面部模型，需要预设 viseme 数据
- 如果你使用的是预设的 `text.usd` 模型，请确保路径正确
- 网络不稳定是导致加载失败的主要原因，可多尝试几次或更换网络



🎉 至此，Audio2Face 安装与配置完成。如果你遇到任何问题，欢迎提交 Issue 或查看常见问题文档。


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

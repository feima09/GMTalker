# GMTalker
<!-- <p align="center">
  <img src="assets/logo.png" alt="项目 Logo" style="width:60%;"/>
</p> -->

<p align="center">
  <a >English</a> | <a href="README_CN.md">中文</a>
</p>

<p align="center">
  <a href="#news">
    <img src="https://img.shields.io/badge/NEWS-Log-red?style=flat-square" />
  </a>
  <a href="#features">
    <img src="https://img.shields.io/badge/Features-Features-blue?style=flat-square" />
  </a>
  <a href="#install">
    <img src="https://img.shields.io/badge/Install-Install-success?style=flat-square" />
  </a>
  <a href="https://huggingface.co/calyi/GMTalker" target="_blank">
    <img src="https://img.shields.io/badge/Hugging-Download-yellow?style=flat-square" />
  </a>
  <a href="https://drive.google.com/file/d/1prydilmo-ftSUjC4L10qylfhr_eYpKYS/view?usp=sharing" target="_blank">
    <img src="https://img.shields.io/badge/UE5_Project-Download-orange?style=flat-square" />
  </a>
</p>

---
**GMTalker**​​, an interactive digital human rendered by Unreal Engine, is developed by the Media Intelligence Team at Bright Laboratory. The system integrates speech recognition, speech synthesis, natural language understanding, and lip-sync animation driving. It supports rapid deployment on Windows and requires only 2GB of VRAM to run the entire project.It can be deployed on Windows, Linux, and Android. This project demonstrates ​​the demo effects of **3D cartoon digital human avatars**​​, suitable for presentations, expansions, and commercial integration.

<!-- System Architecture Diagram -->
<p align="center">
  <img src="assets/jiagou.png" alt="System Architecture Diagram" style="width:80%;"/>
  <br/>
  <em>System Architecture Diagram</em>
</p>

<a name="features"></a>
## 🧱 Features
- Cross-Platform: Deploy on Windows, Linux, and Android with a single codebase.
- Offline & Real-Time: Fully offline streaming dialogue with millisecond response.
- Smart Interaction: Wake-up, interrupt, and voice cloning support.
- Model Flexibility: Compatible with LLMs, custom Agents, and local knowledge bases.
- Avatar Customization: Custom characters with lip-sync and micro-expressions.
- Quick Setup: Easy backend configuration, no extra dependencies needed.
- Hardware Support: Runs on Huawei Ascend NPU or CPU-only mode.

<table align="center">
  <tr>
    <td style="text-align:center">
      <img src="assets/dun.gif" alt="demo1" width="50%" style="display: block; margin: 0 auto;" />
    </td>
    <td style="text-align:center">
      <img src="assets/android.gif" alt="demo2" width="58%" style="display: block; margin: 0 auto;" />
    </td>
  </tr>
</table>

<!-- <table>
  <tr>
    <th align="center">Feature Introduction</th>
    <th align="center">Demonstration Video</th>
  </tr>
  <tr>
    <td><strong>Interrupt</strong><br>Allows users to interrupt conversations in real time via voice, enhancing interaction flexibility</td>
    <td>
      <video src="https://private-user-images.githubusercontent.com/63825035/477330917-45670b4b-a2ee-4345-8365-2a43233e2c8b.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTUwNTAwMzAsIm5iZiI6MTc1NTA0OTczMCwicGF0aCI6Ii82MzgyNTAzNS80NzczMzA5MTctNDU2NzBiNGItYTJlZS00MzQ1LTgzNjUtMmE0MzIzM2UyYzhiLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA4MTMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwODEzVDAxNDg1MFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFhMGZlYWEyOWUyM2RhNDY3YzA1ZjFkZDNlYTNhNTM0NzJiMTMxMWE4NTY5MWRjYmNiZTI1NzlhNGEyMzE1ZGYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.U0ugXLKWtNxhBhBOKYxHMdLD0crRIDZEgz1O9uEsCUM" controls width="70%"></video>
    </td>
  </tr>
</table> -->

<a name="news"></a>
## 🔥 NEWS

- 🗓️ **2025.10.15**: Backend now supports Docker deployment, see [Docker Documentation](./docs/docker.md) for details.
- 🗓️ **2025.10.10**:It now offers comprehensive support for both GPU and NPU 910B servers. The FunASR speech recognition is based on the ONNX Runtime, while the TTS speech synthesis leverages torch_npu.
- 🗓️ **2025.9.12**: The project now offers comprehensive support for Android, Linux, Web, and Windows platforms. With no GPU required on the client side.
- 🗓️ **2025.9.1**: Upgraded the model with a lightweight lip-sync driver and packaged the complete UE project into a standalone executable (.exe), allowing it to run smoothly on ordinary laptops.
- 🗓️ **2025.8.25**: Updated[Import UE avatar](./docs/ue/import_tutorial.md) | [Character Overview](./docs/ue/character_overview.md) | [Animation Overview](./docs/ue/animation_overview.md) documents.
- 🗓️ **2025.8.19**: Released UE5 project files, including the **GuangDUNDUN** character.
  (jointly developed by Guangming Lab and the Shenzhen Guangming District Government).
- 🗓️ **2025.8.12**: Added WebUI usage guide for quick project deployment.


## 💬 Join Our Community

<p align="center">
  <img src="assets/qun.png" alt="GMTalker technical exchange group" width="200"/>
  <br/>
  <strong>Scan QR code to join GMTalker technical exchange group</strong>
</p>

<a name="install"></a>  
## 📦 Quick Start  

#### After configuring the backend, launch the application by downloading the installation package. With FunASR and MeloTTS, it can be started with one click—no additional environment setup or dependencies required.

### ​​Hardware Requirements​  
- **Operating System**: Windows 10+ / Linux
- **Memory**: 8GB+ RAM  
- **GPU Support**: Minimum 2GB VRAM (NVIDIA GPU with CUDA support recommended)

1. **Cloning project**
```bash
git clone  https://github.com/feima09/GMTalker.git
```

2. **One click start**

**Windows:**
```bash
webui.bat
```

**Linux:**
```bash
chmod +x webui.sh
./webui.sh
```

**Docker Deployment (Recommended):**
```bash
# Using docker-compose
docker-compose up -d

# Or using docker cli
docker run -d \
  --name gmtalker \
  -p 5002:5002 -p 7860:7860 \
  -v $(pwd)/configs:/app/configs \
  huiji2333/gmtalker:latest
```
👉 [Docker Deployment Guide](docs/docker.md)

3. **Accessing Services**
- Main service:` http://127.0.0.1:5002 `
- Web configuration interface:` http://127.0.0.1:7860 `

👉 Click here to view the WebUI User [Guide](docs/webui.md)

4. **Download UE Executable​**
- Download and launch GLM3.exe [Windows version Google Drive](https://drive.google.com/file/d/1EO_E33blpLcKop6l1Ta5-PQTCtZVYxLu/view?usp=sharing) [Windows version Baidu Netdisk](https://pan.baidu.com/s/1WbiLS5wyGss_JvUet5mx_g?pwd=w2sb) [Linux version Google Drive](https://drive.google.com/file/d/1ZpKmLAm2yiKJT_4tPzX4VGv7_RNoWNx5/view?usp=sharing) [Linux version Baidu Netdisk](https://pan.baidu.com/s/1adBv9ZYMC5pBhPckaVHJJg?pwd=kit5)

5. **​​Deploy Essential Local AI Services​**
- Download the FunASR speech recognition lazy package [here](https://github.com/1m1ng/FunASR/releases/download/Complete-Package/FunASR.7z), then run run_server_2pass.batto start it with one click.
- Download the MeloTTS speech recognition lazy package [here](https://github.com/1m1ng/MeloTTS/releases/download/Complete-Package/MeloTTS.7z), then run start.batto start it with one click.

👉 If you need to develop from source code, please click here to view the complete installation [guide](docs/install.md),Please refer to the backend overall [architecture](docs/relate.md)


## 📊 Comparison with Other Open-Source Solutions

| Project Name     | 3D Avatar | UE5 Rendering | Voice Input | Voice Interruption | Lip Sync | Body Movements | Local Deployment (Win) | Star ⭐ |
|------------------|:---------:|:-------------:|:-----------:|:-------------------:|:--------:|:--------------:|:-----------------------:|:-------:|
| LiveTalking      | ❌        | ❌            | ❌          | ❌                  | ✅       | ❌             | ❌                      | 6.1k    |
| OpenAvatarChat   | ✅        | ❌            | ✅          | ❌                  | ✅       | ❌             | ❌                      | 1.6k    |
| MNN              | ✅        | ❌            | ✅          | ❌                  | ✅       | ✅             | ❌                      | 12.6k   |
| Fay              | ❌        | ✅            | ✅          | ✅                  | ✅       | ✅             | ✅                      | 11.6k   |
| **GMTalker**     | ✅        | ✅            | ✅          | ✅                  | ✅       | ✅             | ✅                      | 🚀      |

> ✅ indicates full support for the feature, while ❌ indicates it is missing or unsupported.

## 📚 About Guangming Laboratory

The Guangdong Provincial Laboratory of Artificial Intelligence and Digital Economy (Shenzhen) (hereinafter referred to as Guangming Laboratory) is one of the third batch of Guangdong Provincial Laboratories approved for construction by the Guangdong Provincial Government. The laboratory focuses on cutting-edge theories and future technological trends in global artificial intelligence and the digital economy, dedicated to serving major national development strategies and significant needs.

Relying on Shenzhen's industrial, geographical, and policy advantages, Guangming Laboratory brings together global scientific research forces and fully unleashes the agglomeration effect of scientific and technological innovation resources. Centered around the core task of building a domestic AI computing power ecosystem, and driven by the development of multimodal AI technology and its application ecosystem, the laboratory strives to break through key technologies, produce original achievements, and continuously advance technological innovation and industrial empowerment.

The laboratory's goal is to accelerate the supply of diversified applications and full-scenario penetration of artificial intelligence technology, achieving mutual reinforcement of technological innovation and industrial driving forces, and continuously promoting the generation of new quality productivity powered by AI.

---

### 🌐 Contact Us (Project Collaboration)

- Website: [Guangming Laboratory Official Site](https://www.gml.ac.cn/)  
- Email: [mafei@gml.ac.cn](mafei@gml.ac.cn)/[xuhongbo@gml.ac.cn](xuhongbo@gml.ac.cn)     

> **Acknowledgements**  
> Thanks to all team members and partners who participated in the development and support of the GMTalker project. (Fei Ma, Hongbo Xu, Minghui Li, Yiming Luo, Haijun Zhu, Yiyao Zhuo, Chao Song)

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

You are free to use, modify, and share the code and assets for **non-commercial purposes**, provided that you **give appropriate credit**.

🔗 [Full License Text](https://creativecommons.org/licenses/by-nc/4.0/legalcode)  
🔍 [Human-readable Summary](https://creativecommons.org/licenses/by-nc/4.0/)
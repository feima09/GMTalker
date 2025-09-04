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
  <a href="https://drive.google.com/file/d/1756SexJhQDK3Og569RSwkgWDONhj7Zew/view?usp=sharing" target="_blank">
    <img src="https://img.shields.io/badge/UE5_Project-Download-orange?style=flat-square" />
  </a>
</p>

---
**GMTalker**​​, an interactive digital human rendered by Unreal Engine, is developed by the Media Intelligence Team at Bright Laboratory. The system integrates speech recognition, speech synthesis, natural language understanding, and lip-sync animation driving. It supports rapid deployment on Windows and requires only 2GB of VRAM to run the entire project.This project showcases ​​demonstrations of **two 3D cartoon digital human avatars** ​​, suitable for presentations, expansions, and commercial integration.

<p align="center">
  <img src="assets/girl.gif" alt="demo1" width="60%"/>
  <img src="assets/dun.gif" alt="demo2" width="60%"/>
</p>

<table>
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
</table>

<a name="news"></a>
## 🔥 NEWS
- 🗓️ **2025.9.1**: Upgrade the DunDun model with a lightweight lip-sync driver and package the complete Unreal Engine project into an executable (exe) for rapid deployment on a laptop with 2GB VRAM.
- 🗓️ **2025.8.25**: Updated **UE Import Tutorial**, **Character Overview** and **Animation Overview** documents: [import_tutorial.md](./docs/ue/import_tutorial.md) | [character_overview.md](./docs/ue/character_overview.md) | [animation_overview.md](./docs/ue/animation_overview.md)  
- 🗓️ **2025.8.19**: Released UE5 project files, including the **GuangDUNDUN** character
  (jointly developed by Guangming Lab and the Shenzhen Guangming District Government).  
- 🗓️ **2025.8.12**: Added WebUI usage guide for quick project deployment.  
- 🗓️ **2025.8.11**: Added a detailed deployment guide covering C++ environment, CUDA installation, Unreal Engine installation, and Audio2Face setup.  
- 🗓️ **2025.8.5**: Released the backend system of the digital human, supporting both command-line and WebUI startup.  
- 🗓️ **2025.7.22**: Added the configuration process for ASR and TTS.  
- 🗓️ **2025.7.15**: Announced the open-source release of the 3D interactive emotional digital human, supporting local deployment and UE5 rendering.

<!-- ## 📋 TODO List

- [ ] Customized appearance pipeline (covering appearance design, skeleton binding, animation production, and other complete processes)
- [x] Open-source digital human backend system with streaming transmission and support for conversation interruption
- [x] Open-source digital human engineering deployment tutorial -->

## 💬 Join Our Community

<p align="center">
  <img src="assets/qun.png" alt="GMTalker technical exchange group" width="200"/>
  <br/>
  <strong>Scan QR code to join GMTalker technical exchange group</strong>
</p>

### Quick Start
- (Requires: Backend deployment + GLM3.exe + Essential local AI services to run)
1. **Cloning project**
```bash
git clone  https://github.com/feima09/GMTalker.git
```
2. **One click start**
```bash
webui.bat
```
3. **Accessing Services**
- Main service:` http://127.0.0.1:5002 `
- Web configuration interface:` http://127.0.0.1:7860 `

👉 [Click here to view the WebUI User Guide webui.md](docs/webui.md)

4. **Download UE Executable​**
- Download and launch GLM3.exe from: [Project Address](https://drive.google.com/open?id=1N47CF_1zccMb1j2WojdIBrOFBOGLz0zx&usp=drive_fs)

5. **​​Deploy Essential Local AI Services​**
- Download the FunASR speech recognition lazy package [here](https://github.com/1m1ng/FunASR/releases/download/Complete-Package/FunASR.7z), then run run_server_2pass.batto start it with one click.
- Download the MeloTTS speech recognition lazy package [here](https://github.com/1m1ng/MeloTTS/releases/download/Complete-Package/MeloTTS.7z), then run start.batto start it with one click.

👉 [If you need to develop from source code, please click here to view the complete installation guide install.md](docs/install.md)


## 🔁 System Module Interaction Diagram

- Frontend Presentation (UE5 Client)  
- Backend Services (AI Digital Human Backend System)  
- AI Core Service Capabilities (Models + APIs)  
- Environment Management and Deployment Layer (Conda + Local Execution)  

<!-- <p align="center">
  <img src="assets/backend.png" alt="System Architecture Diagram" style="width:100%;"/>
</p> -->

```mermaid
graph TB
    %% Client Layer
    UE5[UE5 Client]
    
    %% Main Service Layer
    subgraph "AI Digital Human Backend System"
        App[Main Application]
        
        %% Core Service Components
        subgraph "Core Services"
            GPT[GPT Service]
            TTS[TTS Service]
            ASR[ASR Service]
            Player[Player Service]
        end
        
        %% Utility Modules
        subgraph "Utility Modules"
            Config[Configuration Management]
            Logger[Log Management]
            Tokenizer[Text Tokenization]
        end
        
        %% Web UI Control Panel
        subgraph "Web UI Control Panel"
            WebUI[webui.py]
            Dashboard[Process Management]
            ConfigUI[Configuration Interface]
        end
    end
    
    %% External Services
    subgraph "External Services"
        OpenAI[OpenAI API<br/>or other LLM]
        FunASR[FunASR<br/>Speech Recognition]
        GPTSOVITS[GPT-SoVITS<br/>TTS Service]
        Audio2Face[Audio2Face<br/>Facial Animation]
    end
    
    %% Connections
    UE5 -.->|Socket.IO<br/>/ue namespace| App
    UE5 -.->|HTTP REST API<br/>/v1/chat/completions| App
    
    App --> GPT
    App --> TTS
    App --> ASR
    App --> Player
    
    GPT -.->|HTTP/HTTPS| OpenAI
    ASR -.->|WebSocket| FunASR
    TTS -.->|HTTP| GPTSOVITS
    Player -.->|gRPC| Audio2Face
    
    App --> Config
    App --> Logger
    App --> Tokenizer
    
    WebUI --> Dashboard
    WebUI --> ConfigUI
    Dashboard -.->|Process Management| App
    
    %% Styling
    classDef clientStyle fill:#e1f5fe
    classDef serviceStyle fill:#f3e5f5
    classDef utilStyle fill:#e8f5e8
    classDef externalStyle fill:#fff3e0
    classDef configStyle fill:#fce4ec
    
    class UE5 clientStyle
    class GPT,TTS,ASR,Player serviceStyle
    class Config,Logger,Tokenizer utilStyle
    class OpenAI,FunASR,GPTSOVITS,Audio2Face externalStyle
```


<a name="features"></a>
## 🧱 Features

- Supports fully offline, real-time streaming conversation services with millisecond-level response
- Supports wake-up and interruption during dialogue, and training/cloning of various voice styles
- Compatible with integration of large models like Qwen and DeepSeek
- Supports connection to local knowledge bases and customization of Agents
- Allows customization of characters, lip-sync driving, and facial micro-expressions such as blinking
- Fully open-source; free of commercial restrictions except for the character, and supports secondary development
- Provides efficient backend configuration services, enabling effortless startup without downloading any additional dependencies


## 📊 Comparison with Other Open-Source Solutions

| Project Name     | 3D Avatar | UE5 Rendering | Voice Input | Voice Interruption | Lip Sync | Body Movements | Local Deployment (Win) | Star ⭐ |
|------------------|:---------:|:-------------:|:-----------:|:-------------------:|:--------:|:--------------:|:-----------------------:|:-------:|
| LiveTalking      | ❌        | ❌            | ❌          | ❌                  | ✅       | ❌             | ❌                      | 6.1k    |
| OpenAvatarChat   | ✅        | ❌            | ✅          | ❌                  | ✅       | ❌             | ❌                      | 1.6k    |
| MNN              | ✅        | ❌            | ✅          | ❌                  | ✅       | ✅             | ❌                      | 12.6k   |
| Fay              | ❌        | ✅            | ✅          | ✅                  | ✅       | ✅             | ✅                      | 11.6k   |
| **GMTalker**     | ✅        | ✅            | ✅          | ✅                  | ✅       | ✅             | ✅                      | 🚀      |

> ✅ indicates full support for the feature, while ❌ indicates it is missing or unsupported.

<a name="install"></a>  
## 📦 Quick Start  

#### After configuring the backend, launch the application by downloading the installation package. With FunASR and MeloTTS, it can be started with one click—no additional environment setup or dependencies required.

### ​​Hardware Requirements​  
- **Operating System**: Windows 10/11 (recommended)  
- **Memory**: 8GB+ RAM  
- **GPU Support**: Minimum 2GB VRAM (NVIDIA GPU with CUDA support recommended)

### Main Configuration Files

- `configs/config.yaml` - Main configuration file  
- `configs/gpt/` - GPT model configuration presets  
- `configs/tts/` - TTS service configuration presets  
- `configs/hotword.txt` - Hotword configuration for wake-up  
- `configs/prompt.txt` - System prompt configuration  

## API Documentation

### REST API

#### POST `/v1/chat/completions`  
Create a new chat session, get AI responses, and play the generated speech.  

**Request Body**:  
```json
{
  "messages": [
    {
      "content": "User input text"
    }
  ],
  "stream": true
}
```

**Response**: 
- Format: `text/event-stream`
- Content: AI reply streaming text

**Response**: 
- Format: `text/event-stream`
- Content: AI's streaming text reply

#### GET `/v1/chat/new`
Create a new chat session.

### SocketIO API

#### Connection Address
```
ws://127.0.0.1:5002/socket.io
```
namespace: `/ue`

#### Event Types

- `question` - Send user question
- `aniplay` - Animation playback control
- `connect/disconnect` - Connection status

## Service Components

### GPT Service (`services/gpt/`)
- **OpenAI Compatible**: Supports OpenAI API format
- **Multi-Model**: Supports OpenAI, Qwen, etc.
- **Streaming Response**: Real-time text stream generation
- **RAG Support**: Configurable Retrieval-Augmented Generation

### TTS Service (`services/tts/`)
- **MeloTTS**: High-quality Chinese speech synthesis
- **Asynchronous Processing**: Handle multiple TTS requests in parallel
- **Fine-tuning & Inference**: Detailed fine-tuning + inference available at [MeloTTS](https://github.com/myshell-ai/MeloTTS) 
- **Weight**: For project-specific voice weights, contact [Contributor](https://github.com/Calylyli)

### ASR Service (`services/asr/`)
- **FunASR Integration**: Speech recognition based on Alibaba's FunASR
- **Wake Word Detection**: Supports custom wake words
- **Real-time Recognition**: Continuous speech recognition mode

### Player Service (`services/player/`)
- **Local Playback**: Local audio playback based on pygame
- **Lip Sync**: Synchronizes speech with facial animation
- **Audio2Face**: [Audio2Face](https://developer.nvidia.cn/omniverse?sortBy=developer_learning_library%2Fsort%2Ffeatured_in.omniverse%3Adesc%2Ctitle%3Aasc&hitsPerPage=6#section-%E5%BC%80%E5%A7%8B%E4%BD%BF%E7%94%A8) requires downloading character models via VPN and has slow initial loading; version 2023.1.1 is recommended.
- **ovrlipsync**: [ovrlipsync](https://developers.meta.com/horizon/documentation/unreal/audio-ovrlipsync-unreal) lightweight lip-sync algorithm with low latency but slightly less effective results.


### 🖼️ User Interaction Flowchart

<!-- <p align="center">
  <img src="assets/flow_chat.png" alt="System Architecture Diagram" style="width:100%;"/>
</p> -->

```mermaid
flowchart TD
    Start([User Starts System]) --> Launch{Launch Method}
    
    %% Launch Method Branch
    Launch -->|Script Launch| Script[Run app.bat/app.ps1]
    Launch -->|Command Line Launch| CLI[python app.py]
    Launch -->|Web Control Panel| WebUI[Run webui.bat/webui.ps1]
    
    Script --> InitCheck[System Initialization Check]
    CLI --> InitCheck
    WebUI --> Dashboard[Web Control Panel]
    
    %% Web Control Panel Flow
    Dashboard --> ConfigPanel{Configuration Panel}
    ConfigPanel --> SetGPT[Configure GPT Service]
    ConfigPanel --> SetTTS[Configure TTS Service]
    ConfigPanel --> SetASR[Configure ASR Service]
    ConfigPanel --> SetPlayer[Configure Player]
    
    SetGPT --> StartServices[Start Services]
    SetTTS --> StartServices
    SetASR --> StartServices
    SetPlayer --> StartServices
    
    %% System Initialization
    InitCheck --> LoadConfig[Load Configuration File]
    LoadConfig --> InitServices[Initialize Service Components]
    InitServices --> StartServer[Start HTTP/Socket.IO Server]
    StartServices --> StartServer
    
    %% User Interaction Method
    StartServer --> UserInteraction{User Interaction Method}
    
    %% HTTP API Interaction
    UserInteraction -->|HTTP API| HTTPRequest[Send Chat Request<br/>/v1/chat/completions]
    HTTPRequest --> ProcessMessage[Process User Message]
    
    %% Socket.IO Interaction (UE5)
    UserInteraction -->|UE5 Socket.IO| UEConnect[UE5 Client Connects<br/>/ue namespace]
    UEConnect --> WaitQuestion[Wait for User Question]
    
    %% Voice Interaction
    UserInteraction -->|Voice Interaction| VoiceWake[Voice Wake-up Detection]
    VoiceWake --> WakeDetected{Wake Word Detected?}
    WakeDetected -->|Yes| VoiceInput[Voice Input to Text]
    WakeDetected -->|No| VoiceWake
    VoiceInput --> ProcessMessage
    
    %% Message Processing Flow
    ProcessMessage --> GPTProcess[GPT Generates Response]
    GPTProcess --> TextStream[Text Stream Output]
    TextStream --> SentenceSplit[Sentence Splitting]
    
    %% Parallel Processing
    SentenceSplit --> TTSConvert[TTS Text-to-Speech]
    SentenceSplit --> ResponseOutput[Real-time Text Response]
    
    TTSConvert --> AudioQueue[Audio Queue]
    AudioQueue --> PlayAudio[Audio Playback]
    
    %% Playback Method Branch
    PlayAudio --> PlayMode{Playback Mode}
    PlayMode -->|Local Playback| LocalPlay[Local Audio Playback]
    PlayMode -->|Audio2Face| A2FPlay[Send to Audio2Face<br/>Facial Animation Sync]
    
    %% Socket.IO Events
    VoiceInput -.->|question event| UEConnect
    LocalPlay -.->|aniplay event| UEConnect
    A2FPlay -.->|aniplay event| UEConnect
    
    %% End or Continue
    LocalPlay --> WaitNext[Wait for Next Interaction]
    A2FPlay --> WaitNext
    ResponseOutput --> WaitNext
    
    WaitNext --> UserInteraction
    
    %% System Monitoring and Management
    StartServer -.-> Monitor[System Monitoring]
    Monitor --> LogOutput[Log Output<br/>logs/YYYY-MM-DD.txt]
    Monitor --> StatusCheck[Status Check]
    
    %% Error Handling
    ProcessMessage --> ErrorHandle{Process Successful?}
    ErrorHandle -->|No| ErrorLog[Error Logging]
    ErrorLog --> WaitNext
    ErrorHandle -->|Yes| TextStream
    
    %% Style Definitions
    classDef startStyle fill:#c8e6c9
    classDef processStyle fill:#bbdefb
    classDef decisionStyle fill:#ffe0b2
    classDef endStyle fill:#ffcdd2
    classDef externalStyle fill:#f3e5f5
    
    class Start,Launch startStyle
    class ProcessMessage,GPTProcess,TTSConvert,PlayAudio processStyle
    class UserInteraction,PlayMode,WakeDetected,ErrorHandle decisionStyle
    class WaitNext endStyle
    class UEConnect,A2FPlay,HTTPRequest externalStyle
```

## 📚 About Guangming Laboratory

The Guangdong Provincial Laboratory of Artificial Intelligence and Digital Economy (Shenzhen) (hereinafter referred to as Guangming Laboratory) is one of the third batch of Guangdong Provincial Laboratories approved for construction by the Guangdong Provincial Government. The laboratory focuses on cutting-edge theories and future technological trends in global artificial intelligence and the digital economy, dedicated to serving major national development strategies and significant needs.

Relying on Shenzhen's industrial, geographical, and policy advantages, Guangming Laboratory brings together global scientific research forces and fully unleashes the agglomeration effect of scientific and technological innovation resources. Centered around the core task of building a domestic AI computing power ecosystem, and driven by the development of multimodal AI technology and its application ecosystem, the laboratory strives to break through key technologies, produce original achievements, and continuously advance technological innovation and industrial empowerment.

The laboratory's goal is to accelerate the supply of diversified applications and full-scenario penetration of artificial intelligence technology, achieving mutual reinforcement of technological innovation and industrial driving forces, and continuously promoting the generation of new quality productivity powered by AI.

---

### 🌐 Contact Us (Project Collaboration)

- Website: [Guangming Laboratory Official Site](https://www.gml.ac.cn/)  
- Email: [mafei@gml.ac.cn](mafei@gml.ac.cn)/[xuhongbo@gml.ac.cn](xuhongbo@gml.ac.cn)     

> **Acknowledgements**  
> Thanks to all team members and partners who participated in the development and support of the GMTalker project. (Fei Ma, Hongbo Xu, Yiming Luo, Minghui Li, Haijun Zhu, Chao Song, Yiyao Zhuo)

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

You are free to use, modify, and share the code and assets for **non-commercial purposes**, provided that you **give appropriate credit**.

🔗 [Full License Text](https://creativecommons.org/licenses/by-nc/4.0/legalcode)  
🔍 [Human-readable Summary](https://creativecommons.org/licenses/by-nc/4.0/)

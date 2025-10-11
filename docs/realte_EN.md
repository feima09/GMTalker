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
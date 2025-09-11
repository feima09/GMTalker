import websockets
import json
import asyncio
from typing import AsyncGenerator
import pyaudio
from utils import config, quartsio, logs
import ssl

logger = logs.get_logger()


class FunASR:
    def __init__(self, socketio: quartsio.QuartSIO) -> None:
        Config = config.Config.get("ASR", {})
        self.url = Config.get("url", "ws://127.0.0.1:10096")
        if self.url.startswith("wss"):
            self.ssl_context = ssl.SSLContext()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
        else:
            self.ssl_context = None
            
        self.status = False
        self.socketio = socketio
        self.is_connected = False

        self.message = json.dumps({
            "mode": "2pass",
            "chunk_size": [5, 10, 5],
            "chunk_interval": 10,
            "wav_name": "microphone",
            "is_speaking": True,
            "hotwords": config.Hotword_msg,
            "itn": True
        })
        
        
        @self.socketio.on("audio_chunk", namespace="/ue")  # type: ignore
        async def audio_chunk(sid, data):
            logger.debug(f"Received audio chunk length: {len(data)}")

            if self.status:
                await websocket.send(data)
                await asyncio.sleep(0.005)
                

    async def connect(self):
        global websocket
        logger.info(f"Connecting to {self.url}")
        while True:
            try: 
                async with websockets.connect(self.url, subprotocols=["binary"], ping_interval=None, ssl=self.ssl_context) as websocket: # type: ignore
                    self.is_connected = True
                    logger.info(f"Connected to {self.url}")
                    await websocket.send(self.message)
                    await websocket.wait_closed()

            except websockets.exceptions.ConnectionClosed:
                logger.info("Connection closed, retrying...")
            except Exception as e:
                logger.error(f"Error connecting to {self.url}: {e}, retrying...")
            finally:
                self.is_connected = False
                self.status = False
                await asyncio.sleep(1)
    
    
    async def receive(self) -> AsyncGenerator[str, None]:
        global websocket
        text_print = ""
        text_print_2pass_online = ""
        text_print_2pass_offline = ""
        
        while True:
            meg = await websocket.recv()
            meg = json.loads(meg)
            text = meg["text"]
            
            if 'mode' not in meg:
                continue
            if meg["mode"] == "2pass-online":
                text_print_2pass_online += "{}".format(text)
                text_print = text_print_2pass_offline + text_print_2pass_online
            else:
                text_print_2pass_online = ""
                text_print = text_print_2pass_offline + "{}".format(text)
                text_print_2pass_offline += "{}".format(text)
            yield text_print


    async def close(self):
        global websocket
        self.is_connected = False
        self.status = False
        await websocket.close()


class FunASRLocal(FunASR):
    def __init__(self) -> None:
        Config = config.Config.get("ASR", {})
        self.url = Config.get("url", "ws://127.0.0.1:10096")
        self.status = False
        self.is_connected = False

        self.message = json.dumps({
            "mode": "2pass",
            "chunk_size": [5, 10, 5],
            "chunk_interval": 10,
            "wav_name": "microphone",
            "is_speaking": True,
            "hotwords": config.Hotword_msg,
            "itn": True
        })
        
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000

        self.loop: asyncio.AbstractEventLoop


    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.status:
            asyncio.run_coroutine_threadsafe(
                websocket.send(in_data),
                self.loop
            )
        return (None, pyaudio.paContinue)


    async def connect(self):
        global websocket
        logger.info(f"Connecting to {self.url}")
        while True:
            try: 
                async with websockets.connect(self.url, subprotocols=["binary"], ping_interval=None) as websocket: # type: ignore
                    self.is_connected = True
                    logger.info(f"Connected to {self.url}")
                    
                    self.loop = asyncio.get_event_loop()
                    
                    p = pyaudio.PyAudio()
                    stream = p.open(
                        format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk,
                        stream_callback=self.audio_callback
                    )
                    
                    await websocket.send(self.message)
                    
                    stream.start_stream()
                    
                    await websocket.wait_closed()

            except websockets.exceptions.ConnectionClosed:
                logger.info("Connection closed, retrying...")
            except Exception as e:
                logger.error(f"Error connecting to {self.url}: {e}, retrying...")
            finally:
                if 'stream' in locals():
                    stream.stop_stream()
                    stream.close()
                if 'p' in locals():
                    p.terminate()
                self.is_connected = False
                self.status = False
                await asyncio.sleep(1)
    
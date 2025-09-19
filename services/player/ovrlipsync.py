from .localplayer import LocalPlayer, logging
import asyncio
import time
    
from utils.quartsio import QuartSIO


class OvrLipSync(LocalPlayer):
    def __init__(self, socketio: QuartSIO):
        self.socketio = socketio
        self.tmp_text = ""
        self.audio_queue = asyncio.Queue()
        self.socketio_queue = asyncio.Queue()
        
        @self.socketio.on("ovrlipsync_receiver", namespace="/ue")  # type: ignore
        async def ovrlipsync_receiver(sid, data):
            if data == self.tmp_text:
                return
            self.tmp_text = data
            logging.info(f"ovrlipsync_receiver: {data}")
            await self.socketio_queue.put(data)


    async def play(self, filename: str):
        logging.info(f"Sending audio file: {filename}")
        try:
            with open(filename, 'rb') as wf:
                data = wf.read()
                
                await self.socketio.emit(
                    "ovrlipsync_sender",
                    data,
                    namespace="/ue"
                )
        except Exception as e:
            logging.error(f"Failed to send audio stream: {e}")
            return
        finally:
            self.remove_audio(filename)


    async def run(self, audio_queue: asyncio.Queue, start_time):
        try:
            audio_file = await audio_queue.get()

            self.audio_queue = audio_queue

            # 记录首次播放的延迟时间（从请求开始到首次音频播放）
            delay = time.time() - start_time
            logging.info(f"First playing audio time: {delay:.2f}s")
                
            # 播放当前音频文件
            await self.play(audio_file)
            
            self.socketio_queue = asyncio.Queue()
            while True:
                await self.socketio_queue.get()
                filename = await audio_queue.get()
                await self.play(filename)
                
                self.audio_queue.task_done()
                self.socketio_queue.task_done()
                
        except asyncio.CancelledError:
            await self.socketio.emit(
                "stop",
                "stop",
                namespace="/ue"
            )
            logging.info("Audio player cancelled")
            raise
            
        finally:
            # 清理队列中剩余的音频文件，避免资源泄露
            while not audio_queue.empty():
                try:
                    filename = audio_queue.get_nowait()
                    if filename is not None:
                        self.remove_audio(filename)
                except asyncio.QueueEmpty:
                    break


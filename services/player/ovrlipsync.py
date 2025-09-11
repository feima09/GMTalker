from .localplayer import LocalPlayer, logging
import asyncio
import time
from pydub import AudioSegment
    
from utils.quartsio import QuartSIO



def get_audio_duration(audio_file) -> float:
    try:
        audio = AudioSegment.from_file(audio_file)
        return len(audio) / 1000.0  # 转换为秒
    except Exception as e:
        print(f"Error: {e}")
        return 0


class OvrLipSync(LocalPlayer):
    def __init__(self, socketio: QuartSIO):
        self.socketio = socketio
        self.tmp_text = ""
        self.audio_queue = asyncio.Queue()
        
        @self.socketio.on("ovrlipsync_receiver", namespace="/ue")  # type: ignore
        async def ovrlipsync_receiver(sid, data):
            if data == self.tmp_text:
                return
            self.tmp_text = data
            logging.info(f"ovrlipsync_receiver: {data}")
            
            self.remove_audio(data)

            filename = await self.audio_queue.get()
            if filename is not None:
                logging.info(f"ovrlipsync_sender: {filename}")
                await self.socketio.emit(
                    "ovrlipsync_sender",
                    filename,
                    namespace="/ue"
                )
        

    async def play(self, filename: str):
        await self.socketio.emit(
            'aniplay', 
            'play',
            namespace='/ue'
        )
        await self.socketio.emit(
            "ovrlipsync_sender",
            filename,
            namespace="/ue"
        )


    async def run(self, audio_queue: asyncio.Queue, start_time):
        try:
            # 从队列中获取下一个要播放的音频文件
            audio_file = await audio_queue.get()
            
            # None作为结束信号，退出播放循环
            if audio_file is None:
                return

            self.audio_queue = audio_queue

            # 记录首次播放的延迟时间（从请求开始到首次音频播放）
            delay = time.time() - start_time
            logging.info(f"First playing audio time: {delay:.2f}s")
                
            # 播放当前音频文件
            await self.play(audio_file)
            # 获取当前音频文件的时长并等待
            duration = get_audio_duration(audio_file)
            await asyncio.sleep(duration)
            
            while not audio_queue.empty():
                await asyncio.sleep(0.1)
                
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
                
                
import asyncio
import pyaudio
import socketio
from queue import Queue

class MicrophoneClient:
    def __init__(self, server_url="http://localhost:5002"):
        self.sio = socketio.AsyncClient()
        self.server_url = server_url
        self.audio_queue = Queue()
        self.is_recording = False
        
        # 音频参数
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        
        self.setup_events()
    
    def setup_events(self):
        @self.sio.event
        async def connect():
            print("已连接到服务器")
            
        @self.sio.event
        async def disconnect():
            print("与服务器断开连接")
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频录制回调函数"""
        if self.is_recording:
            self.audio_queue.put(in_data)
        return (None, pyaudio.paContinue)
    
    async def start_recording(self):
        """开始录音并连接到服务器"""
        try:
            # 连接到服务器
            await self.sio.connect(self.server_url, namespaces=['/ue'])
            
            # 初始化音频
            p = pyaudio.PyAudio()
            stream = p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=self.audio_callback
            )
            
            self.is_recording = True
            stream.start_stream()
            print("开始录音...")
            
            # 发送音频数据
            while self.is_recording:
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get()
                    await self.sio.emit('audio_chunk', audio_data, namespace='/ue')
                await asyncio.sleep(0.001)  # 避免CPU占用过高
                
        except Exception as e:
            print(f"录音错误: {e}")
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            if 'p' in locals():
                p.terminate()
            await self.sio.disconnect()
    
    def stop_recording(self):
        """停止录音"""
        self.is_recording = False

async def main():
    client = MicrophoneClient()
    try:
        await client.start_recording()
    except KeyboardInterrupt:
        print("停止录音...")
        client.stop_recording()

if __name__ == '__main__':
    asyncio.run(main())

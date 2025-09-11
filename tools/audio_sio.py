from utils import quartsio
import asyncio
import pyaudio
from queue import Queue
import threading

app = quartsio.QuartSIO()

# 全局音频播放器
class AudioPlayer:
    def __init__(self):
        self.audio_queue = Queue()
        self.is_playing = False
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.p: pyaudio.PyAudio
        self.stream: pyaudio.Stream

    def start_playback(self):
        """开始音频播放"""
        if self.is_playing:
            return
            
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk
        )
        self.is_playing = True
        
        # 在单独线程中播放音频
        self.playback_thread = threading.Thread(target=self._playback_loop)
        self.playback_thread.daemon = True
        self.playback_thread.start()
        print("音频播放已启动")
    
    def _playback_loop(self):
        """音频播放循环"""
        while self.is_playing:
            try:
                if not self.audio_queue.empty():
                    audio_data = self.audio_queue.get(timeout=1)
                    self.stream.write(audio_data)
            except:
                continue
    
    def add_audio_data(self, data):
        """添加音频数据到播放队列"""
        if self.is_playing:
            self.audio_queue.put(data)
    
    def stop_playback(self):
        """停止音频播放"""
        self.is_playing = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
        print("音频播放已停止")

# 全局音频播放器实例
audio_player = AudioPlayer()


@app.on('connect', namespace='/ue') # type: ignore
async def connect(sid, environ):
    """
    处理Socket.IO连接事件
    
    Args:
        sid: 会话ID
        environ: 环境变量字典
    """
    print(f"客户端已连接: {sid}")
    # 启动音频播放
    audio_player.start_playback()


@app.on('disconnect', namespace='/ue') # type: ignore
async def disconnect(sid):
    """
    处理Socket.IO断连事件
    
    Args:
        sid: 会话ID
    """
    print(f"客户端已断开: {sid}")
    # 停止音频播放
    audio_player.stop_playback()

@app.on('audio_chunk', namespace='/ue') # type: ignore
async def audio_chunk(sid, data):
    """
    处理接收到的音频数据块
    
    Args:
        sid: 会话ID
        data: 音频数据（PCM格式）
    """
    # 将接收到的音频数据添加到播放队列
    audio_player.add_audio_data(data)

if __name__ == '__main__':
    try:
        asyncio.run(app._run())
    except KeyboardInterrupt:
        print("服务器关闭中...")
        audio_player.stop_playback()

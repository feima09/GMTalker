from utils import quartsio
import asyncio
import threading
import queue
import numpy as np
import pygame
import io
import wave
import time

app = quartsio.QuartSIO()
audio_queue = queue.Queue()
is_playing = False
play_thread = None


def audio_player_worker():
    """音频播放工作线程"""
    global is_playing
    
    # 初始化pygame音频混音器
    if not pygame.mixer.get_init():
        pygame.mixer.init(frequency=16000, size=-16, channels=1, buffer=512)
    
    while is_playing:
        try:
            audio_data = audio_queue.get(timeout=1)
            
            if audio_data is None:
                break
                
            play_audio_chunk(audio_data)
            
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Audio player worker error: {e}")


def play_audio_chunk(audio_data):
    """播放单个音频数据块"""
    try:
        if len(audio_data) == 0:
            print("Warning: Received empty audio data")
            return
            
        # 将原始PCM数据转换为numpy数组
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        if len(audio_array) == 0:
            print("Warning: Empty audio array after conversion")
            return
        
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)      # 单声道
            wav_file.setsampwidth(2)      # 16位采样
            wav_file.setframerate(16000)  # 16k采样率
            wav_file.writeframes(audio_array.tobytes())
        
        # 重置缓冲区位置到开头
        wav_buffer.seek(0)
        
        pygame.mixer.music.stop()
        pygame.mixer.music.load(wav_buffer)
        pygame.mixer.music.play()
        
        # 等待播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.01)
            
    except Exception as e:
        print(f"Error playing audio chunk: {e}")
        import traceback
        traceback.print_exc()


def start_audio_player():
    """启动音频播放器"""
    global is_playing, play_thread
    
    if not is_playing:
        is_playing = True
        play_thread = threading.Thread(target=audio_player_worker, daemon=True)
        play_thread.start()
        print("Audio player started")


def stop_audio_player():
    """停止音频播放器"""
    global is_playing, play_thread
    
    if is_playing:
        is_playing = False
        audio_queue.put(None)  # 发送停止信号
        
        if play_thread and play_thread.is_alive():
            play_thread.join(timeout=2)
        
        # 清空队列
        while not audio_queue.empty():
            try:
                audio_queue.get_nowait()
            except queue.Empty:
                break
                
        print("Audio player stopped")


@app.on('connect', namespace='/ue') # type: ignore
async def connet(sid, environ):
    """
    处理Socket.IO连接事件
    
    Args:
        sid: 会话ID
        environ: 环境变量字典
    """
    print(f"Connected: {sid}")
    # 启动音频播放器
    start_audio_player()
    

@app.on('disconnect', namespace='/ue') # type: ignore
async def disconnect(sid):
    """
    处理Socket.IO断连事件
    
    Args:
        sid: 会话ID
    """
    print(f"Disconnected: {sid}")
    # 停止音频播放器
    stop_audio_player()


@app.on('audio_chunk', namespace='/ue') # type: ignore
async def audio_chunk(sid, data):
    """
    处理接收到的音频数据块并加入播放队列
    
    Args:
        sid: 会话ID
        data: 原始音频数据(16k采样率)
    """
    try:
        audio_queue.put(data)
            
    except Exception as e:
        print(f"Error processing audio chunk: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(app._run())
    
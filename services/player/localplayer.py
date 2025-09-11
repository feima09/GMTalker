import pyaudio
import wave
import os
import asyncio
import time

from utils import get_logger

logging = get_logger()


class LocalPlayer:
    """
    本地音频播放器
    
    使用pyaudio库实现的本地音频播放功能，支持异步播放和队列处理。
    主要特性：
    - 基于pyaudio的音频播放
    - 异步播放，不阻塞主线程
    - 自动清理临时音频文件
    - 支持播放队列和任务取消
    - 首次播放时间统计
    
    适用场景：
    - AI数字人的语音输出
    - 实时TTS音频播放
    - 本地部署的语音合成系统
    """
    
    def __init__(self):
        """
        初始化本地播放器
        
        初始化pyaudio实例，为音频播放做准备。
        """
        self.p = pyaudio.PyAudio()
        
        
    @staticmethod
    def remove_audio(filename: str):
        """
        安全删除音频文件
        
        删除指定路径的音频文件，通常用于清理TTS生成的临时文件。
        使用静态方法设计，可以在类的任何地方调用。
        
        Args:
            filename (str): 要删除的音频文件的完整路径
        """
        try:
            os.remove(filename)
        except Exception as e:
            pass    
        
        
    async def play(self, filename: str):
        """
        异步播放单个音频文件
        
        使用pyaudio加载并播放指定的音频文件，播放完成后自动清理文件。
        该方法是播放器的核心功能，实现了完整的播放-清理流程。
        
        Args:
            filename (str): 要播放的音频文件路径
            
        播放流程：
        1. 打开wav音频文件
        2. 获取音频参数
        3. 创建pyaudio流
        4. 分块读取并播放音频数据
        5. 关闭流和文件
        6. 删除临时文件
        
        异常处理：
        - 播放失败时记录错误日志并返回
        - 使用finally确保资源清理
        """
        wf = None
        stream = None
        
        try:
            # 打开wav文件
            wf = wave.open(filename, 'rb')
            
            # 创建音频流
            stream = self.p.open(
                format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            
            # 分块播放音频
            chunk = 1024
            data = wf.readframes(chunk)
            
            while data:
                stream.write(data)
                data = wf.readframes(chunk)
                # 添加小的异步暂停，避免阻塞事件循环
                await asyncio.sleep(0.001)
            
        except Exception as e:
            logging.error(f"Failed to play audio: {e}")
            return
        
        finally:
            # 确保音频资源得到正确释放
            if stream:
                stream.stop_stream()
                stream.close()
            if wf:
                wf.close()
            await asyncio.sleep(0.1)
            self.remove_audio(filename)  
            
            
    async def run(self, audio_queue: asyncio.Queue, start_time):
        """
        运行音频播放队列处理循环
        
        这是播放器的主要运行方法，从队列中持续获取音频文件并依次播放。
        支持性能监控和优雅的任务取消处理。
        
        Args:
            audio_queue (asyncio.Queue): 音频文件队列，TTS服务会将生成的音频文件放入此队列
            start_time (float): 开始时间戳，用于计算首次播放延迟
            
        工作流程：
        1. 从队列中获取音频文件路径
        2. 检查是否为结束信号（None）
        3. 播放音频文件
        4. 记录首次播放时间（性能监控）
        5. 处理任务取消和队列清理
        
        性能特性：
        - 首次播放时间统计：用于评估从请求到首次音频输出的延迟
        - 队列处理：支持流式音频播放，实现近实时的语音合成输出
        - 取消安全：确保任务取消时正确清理剩余音频文件
        """
        # 首次播放标志，用于性能监控
        first_play = True
        
        try:
            while True:
                # 从队列中获取下一个要播放的音频文件
                audio_file = await audio_queue.get()
                
                # None作为结束信号，退出播放循环
                if audio_file is None:
                    break
                    
                # 记录首次播放的延迟时间（从请求开始到首次音频播放）
                if first_play:
                    delay = time.time() - start_time
                    logging.info(f"First playing audio time: {delay:.2f}s")
                    first_play = False
                    
                # 播放当前音频文件
                await self.play(audio_file)
                
        except asyncio.CancelledError:
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
                
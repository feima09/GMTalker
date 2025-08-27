import os
import copy
import time
import random
import string
import asyncio
import aiofiles
import requests

from utils.httpx_client import httpx_client
from utils import get_logger, config

logging = get_logger()
home_dir = os.getcwd()


class GPTSoVits:
    """
    GPT-SoVITS文本转语音服务客户端
    
    这是一个与GPT-SoVITS TTS服务交互的客户端类，提供高质量的语音合成功能。
    GPT-SoVITS是一个基于GPT和SoVITS技术的先进语音合成系统，能够生成自然流畅的语音。
    
    主要功能：
    - 单句文本转语音
    - 流式文本处理和音频生成
    - 性能监控和日志记录
    - 异步处理支持
    - 服务健康检查
    
    技术特点：
    - 使用异步HTTP客户端提高并发性能
    - 支持流式音频生成，实现低延迟播放
    - 完善的错误处理和重试机制
    - 详细的性能指标收集
    """
    
    def __init__(self):
        """
        初始化GPT-SoVITS客户端
        
        从配置文件加载TTS服务的连接参数，创建临时文件目录，
        准备与GPT-SoVITS服务进行通信。
        """
        # 确保临时文件目录存在，用于存储生成的音频文件
        tmp_dir = f"{home_dir}/tmp"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        
        tts_config = config.Config.get("TTS", {})
        
        self.url = tts_config.get("api_endpoint", "")
        
        self.headers = copy.deepcopy(tts_config.get("request_header", {}))
        self.headers["Content-Type"] = "application/json"
        self.headers["Authorization"] = f"Bearer {tts_config.get('api_key', 'empty')}"
        
        self.body = copy.deepcopy(tts_config.get("request_body", ""))
        self.body["streaming_mode"] = False
        
            
    async def generate(self, sentence: str, filename: str):
        """
        生成单个句子的音频文件
        
        将输入的文本发送到GPT-SoVITS服务，获取生成的音频数据并保存为文件。
        包含详细的性能监控，记录请求响应时间和数据传输时间。
        
        Args:
            sentence (str): 需要转换为语音的文本内容
            filename (str): 保存音频文件的完整路径
            
        Raises:
            Exception: 当TTS服务请求失败时抛出，包含详细错误信息
            
        性能指标：
        - 首次响应时间：从发送请求到收到第一个数据包的时间
        - 数据接收时间：从首次响应到所有数据接收完毕的时间
        - 总响应时间：整个请求-响应周期的时间
        """
        # 将要转换的文本设置到请求体中
        self.body['text'] = sentence
        
        try: 
            # 记录请求开始时间
            start_time = time.time()
                
            # 使用流式HTTP请求获取音频数据
            async with httpx_client.stream(
                "POST",
                self.url,
                json=self.body,
                headers=self.headers,
                timeout=30
            ) as response:
                # 记录首次收到响应的时间
                first_repsonse_time = time.time()
                logging.info(f"First received response time: {first_repsonse_time - start_time:.2f}s")
                
                # 检查HTTP响应状态，如果有错误会抛出异常
                response.raise_for_status()
                
                # 异步写入音频数据到文件
                async with aiofiles.open(filename, "wb") as afp:
                    async for chunk in response.aiter_bytes():
                        await afp.write(chunk)
                    
            # 记录所有数据接收完毕的时间
            end_time = time.time()
            logging.info(f"All data received time: {end_time - first_repsonse_time:.2f}s")
            logging.info(f"All response time: {end_time - start_time:.2f}s")    
            
            logging.info(f"Successfully generated audio file: {filename}")
                        
        except Exception as e:
            # 抛出详细的错误信息，便于调试和监控
            raise Exception(f"Failed to request TTS service: {e}")
        
        
    async def audio_generate(self, sentence_stream):
        """
        从句子流中生成音频文件流
        
        这是流式TTS处理的核心方法，接收文本句子流并转换为音频文件流。
        支持实时处理，可以边接收文本边生成音频，大大减少首次播放延迟。
        
        Args:
            sentence_stream (AsyncGenerator): 输入句子的异步生成器，通常来自GPT的流式文本输出
            
        Yields:
            str: 生成的音频文件的完整路径
            None: 流结束标志，用于通知下游组件处理完成
            
        文件命名策略：
        - 使用16位随机字符串作为文件名，避免冲突
        - 统一使用.wav格式，确保兼容性
        - 文件保存在tmp目录下，播放后自动清理
        
        流式处理优势：
        - 减少延迟：不需要等待所有文本生成完毕
        - 提升体验：用户可以更快听到AI的回复
        - 资源优化：分段处理减少内存占用
        """
        index = 0  # 用于调试和日志记录的序号
        
        async for sentence in sentence_stream:
            # None作为流结束标志
            if sentence is None:
                break
                
            index += 1
            
            # 生成随机文件名，确保唯一性
            filename = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            full_path = f"{home_dir}/tmp/" + filename + ".wav"
            
            # 为当前句子生成音频文件
            await self.generate(sentence, full_path)
            
            # 返回生成的音频文件路径
            yield full_path
            
        # 发送结束标志
        yield None


    async def run(self, audio_stream, audio_queue: asyncio.Queue):
        """
        音频生成任务运行器
        
        这是连接TTS生成器和播放器的桥梁方法，负责将生成的音频文件
        传递到播放队列中。支持任务取消和优雅的错误处理。
        
        Args:
            audio_stream (AsyncGenerator): 音频文件路径的异步生成器，来自audio_generate方法
            audio_queue (asyncio.Queue): 音频播放队列，播放器会从中获取音频文件
            
        工作流程：
        1. 从音频流中获取音频文件路径
        2. 将音频文件路径放入播放队列
        3. 处理流结束和任务取消
        4. 确保队列正确结束
        
        异常处理：
        - asyncio.CancelledError: 当任务被取消时（如用户中断），
          会向队列发送结束信号并重新抛出异常
        - 确保无论何种情况下，播放器都能收到结束信号
        """
        try:
            # 遍历音频文件流
            async for audio_file in audio_stream:
                # None标志流结束
                if audio_file is None:
                    break
                # 将音频文件路径放入播放队列
                await audio_queue.put(audio_file)
                
            # 向播放队列发送结束信号
            await audio_queue.put(None)
            
        except asyncio.CancelledError:
            # 处理任务取消（如用户说了新的话，需要中断当前播放）
            logging.info("Audio generator cancelled")
            # 确保播放器收到结束信号，避免无限等待
            await audio_queue.put(None)
            raise


    def test(self):
        """
        TTS服务健康检查
        
        通过发送测试文本来验证GPT-SoVITS服务是否正常工作。
        
        Returns:
            tuple: (成功标志, 消息)
                - (True, "测试通过"): 服务正常
                - (False, 错误信息): 服务异常
                
        测试流程：
        1. 发送固定的测试文本到TTS服务
        2. 检查HTTP响应状态码
        3. 返回测试结果和详细信息
        
        注意：
        - 使用同步requests而非异步httpx，因为这是初始化时的一次性检查
        - 设置较短的超时时间（15秒），避免启动过程阻塞
        - 不保存音频文件，只验证服务连通性
        """
        try:
            self.body['text'] = "这是一条测试信息。"
            
            # 发送同步HTTP请求进行服务测试
            response = requests.post(
                self.url,
                json=self.body,
                headers=self.headers,
                timeout=15
            )
            
            # 检查响应状态码
            if response.status_code != 200:
                raise Exception(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
            else:
                return True, "测试通过"
                
        except Exception as e:
            return False, f"测试失败: {e}"
            

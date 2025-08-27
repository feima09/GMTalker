import requests
import threading

from .wake import Wake
from .realtime import Realtime
from utils import Config, get_logger

logging = get_logger()

host = Config.get("host", "127.0.0.1")
port = Config.get("port", 5002)


def send_request(text):
    """
    向本地服务器发送聊天请求的工具函数
    
    该函数用于在本地模式下，将ASR识别的文本直接发送到本地的聊天API，
    实现语音到文本到AI响应的完整流程。使用流式请求以支持实时响应。
    
    Args:
        text (str): 需要发送给AI的用户语音文本
        
    Note:
        - 使用POST请求调用 /v1/chat/completions 接口
        - 设置30秒超时防止长时间等待
        - 使用流式处理以支持实时响应
        - 异常被静默处理，避免影响主流程
    """
    try:
        # 向本地聊天API发送POST请求
        response = requests.post(
            f"http://{host}:{port}/v1/chat/completions",
            json={"messages": [{"content": text}]},
            timeout=30,
            stream=True
        )
        # 检查HTTP响应状态，如果有错误会抛出异常
        response.raise_for_status()
        
        # 消费流式响应内容
        for chunk in response.iter_content(chunk_size=1024):
            pass
            
    except Exception as e:
        pass


class WakeLocal(Wake):
    """
    本地模式的唤醒词ASR处理器
    
    继承自基础Wake类，增加了本地HTTP请求功能。
    在检测到唤醒词并获取用户语音后，会自动向本地聊天API发送请求，
    实现语音输入到AI响应的完整本地化流程。
    
    特点：
    - 继承所有Wake类的唤醒词检测功能
    - 增加自动发送本地HTTP请求的能力
    - 使用独立线程处理HTTP请求，避免阻塞ASR流程
    - 适用于本地部署的AI聊天系统
    """
    
    async def run(self):
        """
        执行本地模式的完整ASR流程
        
        流程包括：
        1. 调用父类的run方法完成语音识别
        2. 将识别结果通过HTTP请求发送到本地聊天API
        3. 使用独立线程处理HTTP请求，避免阻塞
        
        Returns:
            str: 识别到的用户语音文本
        """
        text = await super().run()
        
        try:
            # 创建独立线程发送HTTP请求，避免阻塞ASR主流程
            thread = threading.Thread(target=send_request, args=(text,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            logging.error(f"Failed to create request thread: {e}")
            

class RealtimeLocal(Realtime):
    """
    本地模式的实时ASR处理器
    
    继承自基础Realtime类，增加了本地HTTP请求功能。
    在实时模式下持续识别用户语音，并自动向本地聊天API发送请求。
    
    特点：
    - 继承所有Realtime类的实时识别功能
    - 增加自动发送本地HTTP请求的能力
    - 使用独立线程处理HTTP请求，避免阻塞ASR流程
    - 适用于需要持续语音交互的本地AI系统
    """
    
    async def run(self):
        """
        执行本地模式的实时ASR流程
        
        流程包括：
        1. 调用父类的run方法完成实时语音识别
        2. 将识别结果通过HTTP请求发送到本地聊天API
        3. 使用独立线程处理HTTP请求，避免阻塞
        
        Returns:
            str: 识别到的用户语音文本
        """
        text = await super().run()
        
        try:
            # 创建独立线程发送HTTP请求，避免阻塞ASR主流程
            thread = threading.Thread(target=send_request, args=(text,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            logging.error(f"Failed to create request thread: {e}")


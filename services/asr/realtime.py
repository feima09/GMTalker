import time
import asyncio

from .wake import Wake
from utils import get_logger

logging = get_logger()


class Realtime(Wake):
    """
    实时语音识别处理器
    
    继承自Wake类，移除了唤醒词检测机制，实现持续的实时语音识别。
    与Wake模式的主要区别：
    - 无需唤醒词，直接开始语音识别
    - 检测到任何语音输入时立即取消其他任务
    - 适用于需要持续语音交互的场景
    
    工作流程：
    1. 启动FunASR进程
    2. 持续监听语音输入
    3. 收到语音时立即取消其他任务
    4. 超时后返回识别结果
    5. 通过Socket.IO发送结果
    """
    
    async def speech(self):
        """
        实时语音识别方法
        
        与Wake类的speech方法不同，这里不需要唤醒词参数，
        直接开始收集用户的语音输入。一旦检测到语音输入，
        立即取消其他正在执行的任务（如音频播放等）。
        
        Returns:
            str: 识别到的完整用户语音文本
            
        Raises:
            Exception: 当语音识别过程出错时抛出
            
        关键特性：
        - 即时响应：检测到语音立即取消其他任务
        - 持续监听：无需唤醒词激活
        - 超时机制：避免无限等待
        """
        # 记录开始时间，用于超时判断
        current_time = time.time()
        text: str = ""
        
        try:
            while True:
                # 检查是否有新的语音识别结果
                if self.parent_conn is not None and self.parent_conn.poll():
                    # 立即取消其他任务
                    self.tasks_cancel_func()
                    
                    # 接收识别结果
                    text = self.parent_conn.recv()
                    logging.info(f"ASR: {text}")
                    
                    # 更新时间戳，表示收到了新的语音输入
                    current_time = time.time()
                    
                # 检查是否超时且有有效文本
                if time.time() - current_time > self.timeout and text:
                    return text
                    
                await asyncio.sleep(0.01)
        except Exception as e:
            logging.error(f"Speech: {e}")
            raise e
    
    
    async def run(self):
        """
        执行一次完整的实时语音识别流程
        
        与Wake类的run方法相比，简化了流程：
        1. 启动FunASR进程
        2. 直接开始语音识别（无需等待唤醒词）
        3. 通过Socket.IO发送识别结果
        4. 清理资源
        
        这种简化的流程使得系统响应更加迅速，
        适用于持续对话和实时交互场景。
        
        Returns:
            str: 识别到的用户语音文本
        """
        self.process_start()
        
        try:
            # 开始语音识别
            text = await self.speech()
            logging.info(f"Recognized text: {text}")
            
            # 通过Socket.IO向客户端发送用户问题
            await self.socketio.emit("question", text, namespace="/ue")
            return text
        finally:
            self.process_stop()
        
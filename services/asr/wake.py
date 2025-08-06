from multiprocessing import Process, Pipe
import socketio
import asyncio
import time

from utils.funasr_wss_client import one_thread
from utils import Config, get_logger

logging = get_logger()
config = Config.get("ASR", "")


class Wake:
    """
    基于唤醒词的语音识别处理器
    
    该类实现了唤醒词检测和语音识别的完整流程：
    1. 持续监听语音输入等待唤醒词
    2. 检测到唤醒词后开始收集用户语音
    3. 在超时后返回识别结果并通过Socket.IO发送
    
    使用多进程架构，通过管道与FunASR WebSocket客户端通信
    """
    
    def __init__(self, socketio: socketio.AsyncServer, tasks_cancel_func):
        """
        初始化Wake实例
        
        Args:
            socketio: Socket.IO异步服务器实例，用于发送识别结果
            tasks_cancel_func: 任务取消函数，用于在检测到唤醒词时清理其他任务
        """
        # 多进程通信管道
        self.parent_conn = None
        self.child_conn = None
        self.process = None
        
        # Socket.IO和任务管理
        self.socketio = socketio
        self.tasks_cancel_func = tasks_cancel_func
        
        # 唤醒词配置：从配置文件读取，支持多个唤醒词
        self.wake_words = config.get("wake_words", "光小明,你好,在吗")
        if isinstance(self.wake_words, str):
            # 将字符串形式的唤醒词转换为列表，去除空白字符
            self.wake_words = [w.strip() for w in self.wake_words.split(",") if w.strip()]
        
        # 语音识别超时时间（秒）
        self.timeout = config.get("timeout", 5)
        
    
    def process_start(self):
        """
        启动FunASR语音识别进程
        
        创建多进程管道并启动FunASR WebSocket客户端进程。
        如果已有进程在运行，会先停止旧进程再启动新进程。
        """
        # 检查并清理已存在的进程和连接
        if self.process is not None and self.process.is_alive():
            self.process_stop()
        if self.parent_conn is not None or self.child_conn is not None:
            self.process_stop()
            
        # 创建父子进程间的双向管道
        self.parent_conn, self.child_conn = Pipe()
        # 启动FunASR处理进程，使用守护进程模式
        self.process = Process(target=one_thread, args=(0, 0, 0, self.child_conn,), daemon=True)
        self.process.start()
        
        
    def process_stop(self):
        """
        停止FunASR语音识别进程并清理资源
        
        按顺序关闭管道连接和进程，确保资源得到正确释放
        """
        # 关闭父进程端管道连接
        if self.parent_conn is not None:
            self.parent_conn.close()
            self.parent_conn = None
            
        # 关闭子进程端管道连接    
        if self.child_conn is not None:
            self.child_conn.close()
            self.child_conn = None
            
        # 终止FunASR进程
        if self.process is not None and self.process.is_alive():
            self.process.terminate()
            self.process = None    
    async def wake(self) -> str:
        """
        等待唤醒词检测
        
        持续监听来自FunASR进程的语音识别结果，
        检查是否包含配置的唤醒词。
        
        Returns:
            str: 检测到的唤醒词
            
        Raises:
            Exception: 当语音识别过程出错时抛出
        """
        try:
            while True:
                # 检查管道是否有数据可读
                if self.parent_conn is not None and self.parent_conn.poll():
                    # 接收FunASR识别结果
                    text: str = self.parent_conn.recv()
                    logging.info(f"ASR: {text}")
                    
                    # 检查文本中是否包含任何配置的唤醒词
                    for word in self.wake_words:
                        if word in text:
                            return word
                            
                await asyncio.sleep(0.01)
        except Exception as e:
            logging.error(f"Wake: {e}")
            raise e
    
    
    async def speech(self, wake_word: str) -> str:
        """
        获取用户语音输入内容
        
        在检测到唤醒词后，持续收集用户的完整语音内容。
        当超过设定的超时时间且有识别结果时，返回去除唤醒词的用户语音内容。
        
        Args:
            wake_word: 已检测到的唤醒词，用于从完整文本中提取用户意图
            
        Returns:
            str: 用户语音内容（已去除唤醒词部分和标点符号）
            
        Raises:
            Exception: 当语音识别过程出错时抛出
        """
        # 记录开始时间，用于超时判断
        current_time = time.time()
        text: str = ""
        
        try:
            while True:
                # 检查是否有新的识别结果
                if self.parent_conn is not None and self.parent_conn.poll():
                    text = self.parent_conn.recv()
                    logging.info(f"ASR: {text}")
                    # 更新时间戳，表示收到了新的语音输入
                    current_time = time.time()
                    
                # 检查是否超时且有有效文本
                if time.time() - current_time > self.timeout and text:
                    # 查找唤醒词在文本中的位置
                    index = text.find(wake_word)
                    # 跳过唤醒词部分
                    index += len(wake_word)
                    
                    # 如果唤醒词后紧跟标点符号，也一并跳过
                    if index < len(text) and text[index] in "，。！？":
                        index += 1
                        
                    # 返回去除唤醒词和标点后的用户语音内容
                    return text[index:]
                    
                await asyncio.sleep(0.01)
        except Exception as e:
            logging.error(f"Speech: {e}")
            raise e

    
    async def run(self) -> str:
        """
        执行一次完整的唤醒词检测和语音识别流程
        
        完整流程包括：
        1. 启动FunASR进程
        2. 等待唤醒词检测
        3. 取消其他正在运行的任务
        4. 收集用户语音内容
        5. 通过Socket.IO发送识别结果
        6. 清理资源
        
        Returns:
            str: 识别到的用户语音文本
        """
        # 启动语音识别进程
        self.process_start()
        
        try:
            # 第一阶段：等待唤醒词
            wake_word = await self.wake()
            logging.info(f"Wake word detected: {wake_word}")
            
            # 检测到唤醒词后取消其他任务（如正在播放的音频等）
            self.tasks_cancel_func()
            
            # 第二阶段：收集用户完整语音
            text = await self.speech(wake_word)
            logging.info(f"Recognized text: {text}")
    
            # 通过Socket.IO向客户端发送用户问题
            await self.socketio.emit("question", text, namespace="/ue")
            
            return text
        finally:
            self.process_stop()
            
    
    async def run_forever(self):
        """
        持续运行唤醒词检测服务
        
        无限循环执行语音识别流程，直到程序终止。
        每次识别完成后会自动开始下一轮检测。
        """
        while True:
            await self.run()

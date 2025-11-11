from .funasr import FunASR, FunASRLocal
from utils import config, quartsio, logs
import asyncio
import requests
import threading
from utils.task import TaskManager

logging = logs.get_logger()


class Wake:
    def __init__(self, socketio: quartsio.QuartSIO, tasks: TaskManager, funasr: FunASR) -> None:
        Config = config.Config.get("ASR", {})
        self.wake_words = Config.get("wake_words", "光小明,你好,在吗")
        if isinstance(self.wake_words, str):
            # 将字符串形式的唤醒词转换为列表，去除空白字符
            self.wake_words = [w.strip() for w in self.wake_words.split(",") if w.strip()]
        self.timeout = Config.get("timeout", 5)
        
        self.socketio = socketio
        self.tasks = tasks
        self.interrupt = Config.get("interrupt", False)
        
        self.funasr = funasr
        asyncio.create_task(self.funasr.connect())
        
        
    async def wake(self) -> str:
        wake_word = ""
        try:
            self.funasr.status = True
            async for text in self.funasr.receive():
                logging.info(text)
                
                # 检查文本中是否包含任何配置的唤醒词
                for word in self.wake_words:
                    if word in text:
                        wake_word = word
                        break
                    
                if wake_word:
                    break
            return wake_word
        except Exception as e:
            logging.error(f"Error in wake: {e}")
            raise e
        finally:
            await self.funasr.receive().aclose()
            self.funasr.status = False


    async def speech(self) -> str:
        text = ""
        queue = asyncio.Queue()

        async def collect_text():
            self.funasr.status = True
            async for data in self.funasr.receive():
                logging.info(data)
                await queue.put(data)

        try:
            task = asyncio.create_task(collect_text())
            while True:
                if text == "":
                    text = await queue.get()
                else:
                    text = await asyncio.wait_for(queue.get(), timeout=self.timeout)
        except asyncio.TimeoutError:
            # 如果text文本第一个是标点符号
            if text[0] in "，。！？":
                return text[1:]
            return text
        except Exception as e:
            logging.error(f"Error in speech: {e}")
            raise e
        finally:
            task.cancel()
            await self.funasr.receive().aclose()
            self.funasr.status = False


    @staticmethod
    def send_request(text):
        """
        向本地服务器发送聊天请求的工具函数
        
        该函数用于在本地模式下，将ASR识别的文本直接发送到本地的聊天API，
        实现语音到文本到AI响应的完整流程。使用流式请求以支持实时响应。
        
        Args:
            text (str): 需要发送给AI的用户语音文本
            
        Note:
            - 使用POST请求调用 /v1/chat/completions 接口
            - 设置更长超时防止长时间等待
            - 使用流式处理以支持实时响应
            - 异常被静默处理，避免影响主流程
        """
        try:
            # 向本地聊天API发送POST请求
            response = requests.post(
                f"http://{config.Config.get('host', '127.0.0.1')}:{config.Config.get('port', 5002)}/v1/chat/completions",
                json={"messages": [{"content": text}]},
                timeout=600,
                stream=True,
                headers={
                    'Connection': 'keep-alive',
                    'Keep-Alive': f'timeout=300'
                }
            )
            # 检查HTTP响应状态，如果有错误会抛出异常
            response.raise_for_status()
            
            # 消费流式响应内容
            for chunk in response.iter_content(chunk_size=1024):
                pass
                
        except Exception as e:
            logging.error(f"Error sending request: {e}")
            pass


    async def send_question(self, text: str):
        if isinstance(self.funasr, FunASRLocal):
            try:
                # 创建独立线程发送HTTP请求，避免阻塞ASR主流程
                thread = threading.Thread(target=self.send_request, args=(text,))
                thread.daemon = True
                thread.start()
            except Exception as e:
                logging.error(f"Failed to create request thread: {e}")
        else:
            await self.socketio.emit("question", text, namespace="/ue")


    async def run(self):
        # 第一阶段：等待唤醒词
        logging.info("Waiting for wake word...")
        wake_word = await self.wake()
        logging.info(f"Wake word detected: {wake_word}")
        
        # 检测到唤醒词后取消其他任务（如正在播放的音频等）
        self.tasks.cancel_all()
        
        await asyncio.sleep(0.1)
        
        # 第二阶段：收集用户完整语音
        logging.info("Collecting user speech...")
        text = await self.speech()
        logging.info(f"Recognized text: {text}")
        
        # 过滤文本：只保留唤醒词及之后的内容
        if wake_word and wake_word in text:
            wake_index = text.find(wake_word)
            text = text[wake_index + len(wake_word):].strip()
        
        # 发送问题
        await self.send_question(text)

    
    async def run_forever(self):
        while True:
            if self.funasr.is_connected:
                await self.run()
                
                if not self.interrupt:
                    await asyncio.sleep(1)
                    player_task = self.tasks.get_tasks(tag="player")
                    if player_task:
                        await player_task
                        
            await asyncio.sleep(0.1)

"""
主程序入口脚本

启动方法：python app.py
"""

import os
import time
import asyncio

from quart import Quart, request, jsonify, Response
from quart_cors import cors
import socketio

from utils import Config, get_logger, atee, sentence_segment
from services.gpt import GPT
from services.tts import TTS
from services.player import Player

logging = get_logger()
home_dir = os.getcwd()

# CORS配置：允许所有来源的跨域请求
CORS_ALLOWED_ORIGINS = "*"

host = Config.get("host", "127.0.0.1")
port = Config.get("port", 5002)


class QuartSIO:
    """
    整合了Quart和Socket.IO的服务器应用类
    
    该类将Quart web框架和Socket.IO实时通信功能集成在一起，
    提供HTTP API接口和WebSocket实时通信能力。
    支持跨域请求和异步处理。
    """
    
    def __init__(self):
        """初始化QuartSIO实例，配置Socket.IO服务器、Quart应用和CORS"""
        self._sio = socketio.AsyncServer(
            async_mode='asgi', 
            cors_allowed_origins=CORS_ALLOWED_ORIGINS
        )
        self._quart_app = Quart(__name__)
        self._quart_app = cors(
            self._quart_app, 
            allow_origin=CORS_ALLOWED_ORIGINS
        )
        self._sio_app = socketio.ASGIApp(
            self._sio, 
            self._quart_app
        )
        self.route = self._quart_app.route
        self.on = self._sio.on
        self.emit = self._sio.emit
        
    async def _run(self):
        """
        启动服务器的内部异步方法
        
        使用Hypercorn ASGI服务器启动应用，配置了：
        - 绑定地址和端口
        - 单工作进程
        - 超时设置为300秒
        - 保持连接超时为300秒
        
        处理键盘中断（Ctrl+C）以优雅关闭服务器
        """
        import hypercorn.asyncio
        try:
            await hypercorn.asyncio.serve(
                    self._sio_app,
                    hypercorn.Config.from_mapping(
                        bind=f"{host}:{port}",
                        workers=1,
                        timeout=300,
                        keep_alive_timeout=300
                    )
                )
        except KeyboardInterrupt:
            logging.info("Shutting down server")
        finally:
            logging.info("Server stopped")
    
    def run(self):
        """
        启动服务器的公共方法
        
        创建并运行事件循环来执行异步服务器
        """
        asyncio.run(self._run())


app = QuartSIO()


# 全局任务集合，用于跟踪和管理所有正在运行的异步任务
tasks = set()
def tasks_cancel():
    """
    取消并清理所有正在运行的异步任务
    
    该函数遍历全局tasks集合中的所有异步任务,
    对每个任务执行取消操作并标记为完成。
    主要用于在开始新对话或应用关闭时确保没有遗留的任务继续运行。
    """
    global tasks
    task: asyncio.Task
    for task in tasks:
        if not task.done():
            task.cancel()
    tasks.clear()


@app.on('connect', namespace='/ue') # type: ignore
async def connet(sid, environ):
    """
    处理Socket.IO连接事件
    
    Args:
        sid: 会话ID
        environ: 环境变量字典
    """
    logging.info(f"Connected: {sid}")
    

@app.on('disconnect', namespace='/ue') # type: ignore
async def disconnect(sid):
    """
    处理Socket.IO断连事件
    
    Args:
        sid: 会话ID
    """
    logging.info(f"Disconnected: {sid}")


@app.route('/v1/chat/completions', methods=['POST'])
async def chat():
    """
    处理聊天完成请求的API端点
    
    该端点接收用户消息，通过GPT生成响应，同时进行文本转语音和音频播放。
    使用流式处理以实现实时响应。
    
    Returns:
        Response: 流式响应对象，包含GPT生成的文本数据
    """
    global tasks
    # 取消之前的任务，确保新对话开始时清理旧任务
    tasks_cancel()
    
    # 解析请求数据
    data: dict = await request.json
    messages: list[dict] = data.get("messages", [])
    if not messages:
        return jsonify({"error": "Message is required"}), 400
    message = messages[0].get("content", "")
    
    # 记录开始时间，用于音频播放同步
    start_time = time.time()
    
    async def generate():
        """
        内部异步生成器函数，处理GPT文本生成、TTS转换和音频播放的并发流程
        
        流程说明：
        1. 启动GPT流式文本生成
        2. 将文本流分成两路：一路用于分句TTS，一路用于输出
        3. 分句后的文本送入TTS进行语音合成
        4. 音频数据通过队列传递给播放器
        5. 同时输出GPT生成的文本流
        """
        # 启动GPT流式生成
        gpt_stream = gpt.generate_stream(message)
        
        # 将GPT流分成两个独立的流
        stream1, stream2, task = await atee(gpt_stream)
        tasks.add(task)
        
        # 将第一个流进行分句处理，为TTS做准备
        sentence_stream = sentence_segment(gpt.create_text_stream(stream1))
        
        # 启动TTS音频生成流
        audio_stream = tts.audio_generate(sentence_stream)
        
        # 创建音频队列用于TTS和播放器之间的数据传递
        audio_queue = asyncio.Queue()
                        
        # 创建TTS音频生成任务
        audio_gen_task = asyncio.create_task(tts.run(audio_stream, audio_queue))
        tasks.add(audio_gen_task)
        
        # 创建音频播放任务
        play_task = asyncio.create_task(player.run(audio_queue, start_time))
        tasks.add(play_task)
        
        # 创建输出流，用于返回给客户端
        output_stream = gpt.output_stream(stream2)
                    
        try:
            # 流式输出GPT生成的文本
            async for data in output_stream:
                yield data
            
            # 等待音频生成和播放任务完成
            await audio_gen_task
            await play_task
        except asyncio.CancelledError:
            # 处理任务取消情况
            logging.info("Chat cancelled")
            audio_gen_task.cancel()
            play_task.cancel()
            raise
        else:
            # 正常完成后清理任务集合
            tasks.clear()
    
    try:
        # 返回流式响应
        return Response(
            generate(),
            mimetype="text/event-stream"
        )
    except Exception as e:
        logging.error(f"Failed to chat: {e}")
        return jsonify({"error": f"Failed to chat: {e}"}), 500


@app.route('/v1/chat/new', methods=['GET'])
async def new_chat():
    """
    开始新对话的API端点
    
    清理所有正在运行的任务并重置GPT状态，
    为新的对话会话做准备。
    
    Returns:
        dict: 包含成功消息的JSON响应
    """
    tasks_cancel()    # 取消所有运行中的任务
    GPT.reset_body()  # 重置GPT的对话状态
    return jsonify({"message": "New chat started"}), 200


if __name__ == '__main__':
    """
    应用程序入口点
    
    初始化各个服务组件并启动应用：
    1. 创建GPT、TTS、Player服务实例
    2. 根据配置决定是否启用ASR（自动语音识别）服务
    3. 启动服务器并处理优雅关闭
    """
    # 初始化核心服务组件
    gpt = GPT()
    tts = TTS()
    player = Player(app)
    
    # ASR任务引用，用于后续清理
    asr_task = None
    
    async def main():
        """
        主异步函数，处理服务启动逻辑
        """
        if Config.get("ASR", "").get("enable", False):
            global asr_task
            from services.asr import ASR
            asr = ASR(app, tasks_cancel)
            asr_task = asyncio.create_task(asr.run_forever())
        
        await app._run()
    
    try:
        asyncio.run(main())
    finally:
        if asr_task:
            asr_task.cancel()

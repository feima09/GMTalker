"""
主程序入口脚本

启动方法：python app.py
"""

import os
import time
import asyncio
from quart import request, jsonify, Response

from utils import Config, get_logger, atee, sentence_segment
from utils.quartsio import QuartSIO
from utils.task import TaskManager
from services.gpt import GPT
from services.tts import TTS
from services.player import Player

logging = get_logger()
home_dir = os.getcwd()
app = QuartSIO()

# 创建全局任务管理器实例
tasks = TaskManager()


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
    tasks.cancel_all()
    
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
        tasks.add(task, tag="gpt")
        
        # 将第一个流进行分句处理，为TTS做准备
        sentence_stream = sentence_segment(gpt.create_text_stream(stream1))
        
        # 启动TTS音频生成流
        audio_stream = tts.audio_generate(sentence_stream)
        
        # 创建音频队列用于TTS和播放器之间的数据传递
        audio_queue = asyncio.Queue()
                        
        # 创建TTS音频生成任务
        audio_gen_task = asyncio.create_task(tts.run(audio_stream, audio_queue))
        tasks.add(audio_gen_task, tag="tts")
        
        # 创建音频播放任务
        play_task = asyncio.create_task(player.run(audio_queue, start_time))
        tasks.add(play_task, tag="player")

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
            
            raise
        else:
            # 正常完成后清理任务
            tasks.clear()
    
    try:
        # 返回流式响应
        return Response(
            generate(),
            mimetype="text/event-stream",
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Keep-Alive': f'timeout=300'
            }
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
    tasks.cancel_all()  # 取消所有运行中的任务
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
            asr = ASR(app, tasks)
            asr_task = asyncio.create_task(asr.run_forever())
        
        await app._run()
    
    try:
        asyncio.run(main())
    finally:
        if asr_task:
            asr_task.cancel()

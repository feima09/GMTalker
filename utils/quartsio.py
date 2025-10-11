import socketio
from quart import Quart
from quart_cors import cors
import asyncio

from .logs import get_logger
from .config import Config

logging = get_logger()
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
            cors_allowed_origins=CORS_ALLOWED_ORIGINS,
            ping_timeout=300,
            ping_interval=30,
            max_http_buffer_size=10**8
        )
        self._quart_app = Quart(__name__)
        
        # 配置Quart应用超时时间
        self._quart_app.config.update({
            'SEND_FILE_MAX_AGE_DEFAULT': 300,
            'PERMANENT_SESSION_LIFETIME': 300,
            'RESPONSE_TIMEOUT': 300,
            'REQUEST_TIMEOUT': 300,
        })
        
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
                        keep_alive_timeout=300,
                        graceful_timeout=120,
                        max_request_size=16777216,
                        max_request_line_size=8192
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


import gradio as gr
from time import sleep
import requests
import os
import threading

from .utils import ProcessManager
from .common import update_logs, get_status, clear_logs, REFRESH_INTERVAL, save_config
from utils.config import Webui as Config

process = ProcessManager("Audio2Face")


def load_config():
    sleep(10)
    
    while True:
        try:
            response = requests.get(
                url="http://localhost:8011/status",
                timeout=5
            )
            if response.status_code == 200:
                break
        except requests.RequestException:
            pass
        
        sleep(3)
        
    try:
        response = requests.post(
            url="http://localhost:8011/A2F/USD/Load",
            json={
                "file_name": Config.get("audio2face", {}).get("usd_path", "")
            },
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        return f"加载Audio2Face USD配置文件失败: {e}"
        
        
thread = threading.Thread(target=load_config)
thread.daemon = True


def start_process() -> str:
    process.start_process(os.path.join(Config.get("audio2face", {}).get("path", ""), "audio2face.bat"))
    thread.start()
        
    return process.process_name + "服务已启动"


def stop_process() -> str:
    process.stop_process()
    thread.join(timeout=3)
    return process.process_name + "服务已停止"


def save_path(path, usd_path) -> str:
    save_config("audio2face_path", path)
    save_config("audio2face_usd_path", usd_path)
    return "路径已保存"


def create_ui():
    with gr.Row():
        with gr.Column(scale=1):
            start_btn = gr.Button("启动" + process.process_name + "服务", variant="primary")
            stop_btn = gr.Button("停止" + process.process_name + "服务", variant="stop")
            clear_logs_btn = gr.Button("清空日志")
            
            status_label = gr.Markdown("## 进程状态")
            status_info = gr.JSON(value=get_status(process), label="状态信息")
            
        with gr.Column(scale=2):
            logs_label = gr.Markdown("## 控制台日志")
            a2f_logs_output = gr.Textbox(
                label="实时日志输出", 
                lines=25,
                max_lines=25,
                autoscroll=True
            )
        
        # 设置按钮回调
        start_btn.click(
            fn=start_process,
            outputs=a2f_logs_output
        )
        stop_btn.click(
            fn=stop_process,
            outputs=a2f_logs_output
        )
        clear_logs_btn.click(
            fn=lambda: clear_logs(process),
            outputs=a2f_logs_output
        )
        
        # 创建定时器组件并使用tick方法设置定时调用
        log_timer = gr.Timer(value=REFRESH_INTERVAL, active=True)
        log_timer.tick(
            fn=lambda: update_logs(process),
            inputs=None,
            outputs=a2f_logs_output
        )
        
        status_timer = gr.Timer(value=REFRESH_INTERVAL, active=True)
        status_timer.tick(
            fn=lambda: get_status(process), 
            inputs=None, 
            outputs=status_info
        )
        

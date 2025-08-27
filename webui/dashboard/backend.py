import gradio as gr
import os

from .utils import ProcessManager
from .common import update_logs, get_status, clear_logs, REFRESH_INTERVAL

ROOT_PATH = os.getcwd()
process = ProcessManager("Backend")


def start_process() -> str:
    process.start_process(os.path.join(ROOT_PATH, "app.py"))
    return process.process_name + "服务已启动"


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
            logs_output = gr.Textbox(
                label="实时日志输出", 
                lines=25,
                max_lines=25,
                autoscroll=True
            )
        
        # 设置按钮回调
        start_btn.click(
            fn=start_process,
            outputs=logs_output
        )
        stop_btn.click(
            fn=process.stop_process,
            outputs=logs_output
        )
        clear_logs_btn.click(
            fn=lambda: clear_logs(process),
            outputs=logs_output
        )
        
        # 创建定时器组件并使用tick方法设置定时调用
        log_timer = gr.Timer(value=REFRESH_INTERVAL, active=True)
        log_timer.tick(
            fn=lambda: update_logs(process),
            inputs=None,
            outputs=logs_output
        )
        
        status_timer = gr.Timer(value=REFRESH_INTERVAL, active=True)
        status_timer.tick(
            fn=lambda: get_status(process), 
            inputs=None, 
            outputs=status_info
        )
        

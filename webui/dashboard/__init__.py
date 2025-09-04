import gradio as gr

from . import backend, audio2face, ue5, config
from utils.config import Webui as Config


def start_all_services() -> str:
    backend.start_process()
    if Config.get("audio2face", {}).get("enable", False):
        audio2face.start_process()
    if Config.get("ue5", {}).get("enable", False):
        ue5.start_process()
    return "所有服务已启动"


def stop_all_services() -> str:
    backend.process.stop_process()
    audio2face.process.stop_process()
    ue5.process.stop_process()
    return "所有服务已停止"


def create_ui():
    """
    创建Gradio用户界面
    
    Returns:
        gr.Blocks: Gradio界面对象
    """
    gr.Markdown("# AI数字人控制面板")
    with gr.Row():
        with gr.Column(scale=1):
            start_btn = gr.Button("一键启动服务", variant="primary")
            stop_btn = gr.Button("一键停止服务", variant="stop")
            
        with gr.Column(scale=2):
            status_output = gr.Textbox(
                label="结果输出",
                lines=1,
                max_lines=1,
                autoscroll=True
            )
            
        start_btn.click(
            fn=start_all_services,
            outputs=status_output
        )
        stop_btn.click(
            fn=stop_all_services,
            outputs=status_output
        )
            
    with gr.TabItem("后端",):
        backend.create_ui()

    with gr.TabItem("Audio2Face", visible=Config.get("audio2face", {}).get("enable", False)) as audio2face_tab:
        audio2face.create_ui()

    with gr.TabItem("UE5", visible=Config.get("ue5", {}).get("enable", False)) as ue5_tab:
        ue5.create_ui()
        
    with gr.TabItem("配置"):
        config.create_ui(audio2face_tab, ue5_tab)
        

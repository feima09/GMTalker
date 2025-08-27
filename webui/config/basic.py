import gradio as gr

from utils import config

def create_ui() -> list:
    Config = config.Config
    
    with gr.TabItem("基本配置"):
        with gr.Group():
            with gr.Row():
                log_level = gr.Dropdown(
                    choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                    value=Config.get("log_level", "INFO"),
                    label="日志等级",
                    interactive=True
                )
                host = gr.Textbox(
                    value=Config.get("host", "0.0.0.0"),
                    label="服务器主机",
                    interactive=True
                )
                port = gr.Number(
                    value=Config.get("port", 5002),
                    label="服务器端口",
                    precision=0,
                    interactive=True
                )

    return [log_level, host, port]


def save_config(log_level, host, port) -> dict:
    config = {
        "log_level": log_level,
        "host": host,
        "port": port
    }
    return config


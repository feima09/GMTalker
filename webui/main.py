import gradio as gr

from . import dashboard, config


def create_ui() -> gr.Blocks:
    """
    创建Gradio UI界面
    
    Returns:
        gr.Blocks: Gradio Blocks对象
    """
    with gr.Blocks(title="AI数字人控制面板") as main:
       with gr.Tabs():
            with gr.TabItem("控制面板"):
                dashboard.create_ui()
            
            with gr.TabItem("配置面板"):
                config.create_ui()
            
    return main


webui = create_ui()

if __name__ == "__main__":
    webui.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True
    )

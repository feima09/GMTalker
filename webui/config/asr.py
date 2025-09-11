import gradio as gr

from utils import config


def create_ui() -> list:
    asr_config = config.Config.get("ASR", {})
    
    with gr.TabItem("ASR配置"):
        with gr.Group():
            asr_enable = gr.Checkbox(
                value=asr_config.get("enable", False),
                label="启用语音识别"
            )
            
            with gr.Group(visible=asr_enable.value) as asr_settings_group:
                url = gr.Textbox(
                    value=asr_config.get("url", "ws://127.0.0.1:10096"),
                    label="服务器URL"
                )
                asr_mode = gr.Radio(
                    choices=["wake", "realtime"],
                    value=asr_config.get("mode", "wake"),
                    label="识别模式"
                )
                
                with gr.Row():
                    timeout = gr.Slider(
                        minimum=0.1,
                        maximum=60.0,
                        value=asr_config.get("timeout", 1.0),
                        step=0.1,
                        label="超时时间（秒）"
                    )
                    wake_words = gr.Textbox(
                        value=asr_config.get("wake_words", []),
                        label="唤醒词（用英文逗号分隔）",
                        visible=asr_mode.value == "wake"
                    )
                    
                    asr_mode.change(
                        fn=lambda x: gr.update(visible=(x == "wake")),
                        inputs=asr_mode,
                        outputs=wake_words
                    )
            
            asr_enable.change(
                fn=lambda x: gr.Group(visible=x),
                inputs=asr_enable,
                outputs=asr_settings_group
            )

    return [asr_enable, url, asr_mode, wake_words, timeout]


def save_config(asr_enable, url, asr_mode, wake_words, timeout) -> dict:
    asr_config = {
        "enable": asr_enable,
        "url": url,
        "mode": asr_mode,
        "wake_words": wake_words,
        "timeout": timeout
    }
    return asr_config


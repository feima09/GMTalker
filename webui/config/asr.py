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
                
                with gr.Accordion("FunASR配置"):
                    funasr_config = asr_config.get("FunASR", {})
                    
                    with gr.Row():
                        funasr_ip = gr.Textbox(
                            value=funasr_config.get("ip", ""),
                            label="IP"
                        )
                        funasr_port = gr.Number(
                            value=funasr_config.get("port", ""),
                            label="Port",
                            precision=0
                        )
                        funasr_mode = gr.Textbox(
                            value=funasr_config.get("mode", ""),
                            label="模式"
                        )
                    
                    funasr_ssl = gr.Checkbox(
                        value=bool(funasr_config.get("ssl", 0)),
                        label="启用SSL"
                    )
            
            asr_enable.change(
                fn=lambda x: gr.Group(visible=x),
                inputs=asr_enable,
                outputs=asr_settings_group
            )

    return [
        asr_enable, asr_mode, wake_words, timeout,
        funasr_ip, funasr_port, funasr_ssl, funasr_mode
    ]


def save_config(asr_enable, asr_mode, wake_words, timeout,
                funasr_ip, funasr_port, funasr_ssl, funasr_mode) -> dict:
    asr_config = {
        "enable": asr_enable,
        "mode": asr_mode,
        "wake_words": wake_words,
        "timeout": timeout,
        "FunASR": {
            "ip": funasr_ip,
            "port": funasr_port,
            "ssl": 1 if funasr_ssl else 0,
            "mode": funasr_mode
        }
    }
    return asr_config


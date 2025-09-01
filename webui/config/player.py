import gradio as gr

from utils import config


def create_ui() -> list:
    player_config = config.Config.get("Player", {})
    
    with gr.TabItem("Player配置"):
        with gr.Group():
            player_mode = gr.Radio(
                choices=["local", "audio2face", "ovrlipsync"],
                value=player_config.get("mode", "local"),
                label="播放器模式"
            )

            with gr.Accordion("Audio2Face配置", visible=player_mode.value == "audio2face") as a2f_config_group:
                a2f_config = player_config.get("Audio2Face", {})
                
                with gr.Row():
                    a2f_url = gr.Textbox(
                        value= a2f_config.get("url", ""),
                        label="Audio2Face URL"
                    )
                    a2f_player = gr.Textbox(
                        value= a2f_config.get("player", ""),
                        label="Audio2Face播放器路径"
                    )
                    
            player_mode.change(
                fn=lambda x: gr.update(visible=(x == "audio2face")),
                inputs=player_mode,
                outputs=a2f_config_group
            )
            
    return [player_mode, a2f_url, a2f_player]


def save_config(player_mode, a2f_url, a2f_player) -> dict:
    player_config = {
        "mode": player_mode,
        "Audio2Face": {
            "url": a2f_url,
            "player": a2f_player
        }
    }
    
    return player_config


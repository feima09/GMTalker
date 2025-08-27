import gradio as gr

from . import basic, gpt, tts, asr, player
from utils import config


def create_ui():
    gr.Markdown("# AI数字人后端配置")
    
    components = []
    
    with gr.Tabs():
        # 基本配置
        basic_components = basic.create_ui()
        components.extend(basic_components)
        # GPT配置
        gpt_components = gpt.create_ui()
        components.extend(gpt_components)
        # TTS配置
        tts_components = tts.create_ui()
        components.extend(tts_components)
        # ASR配置
        asr_components = asr.create_ui()
        components.extend(asr_components)
        # 播放器配置
        player_components = player.create_ui()
        components.extend(player_components)
        
    # 单一保存按钮
    save_button = gr.Button("保存所有配置", variant="primary", size="lg")
    save_output = gr.Textbox(label="保存结果")
    
    
    def save_all_configs(*args):
        index_a = len(basic_components)
        Config = basic.save_config(*args[:index_a])
        index_b = index_a + len(gpt_components)
        Config["GPT"] = gpt.save_config(*args[index_a:index_b])
        index_a = index_b + len(tts_components)
        Config["TTS"] = tts.save_config(*args[index_b:index_a])
        index_b = index_a + len(asr_components)
        Config["ASR"] = asr.save_config(*args[index_a:index_b])
        Config["Player"] = player.save_config(*args[index_b:])
        
        config.save_config(Config, "config.yaml")
        return "所有配置已保存成功！"
    
    
    save_button.click(
        fn=save_all_configs,
        inputs=[comp for comp in components],
        outputs=save_output
    )

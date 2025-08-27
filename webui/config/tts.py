import gradio as gr
import json

from utils import config
from .common import get_preset_configs, load_preset_config, save_preset_config


def create_ui() -> list:
    tts_config = config.Config.get("TTS", {})
    
    with gr.TabItem("TTS配置"):
        with gr.Group():
            # 预设配置管理
            with gr.Accordion("预设配置管理", open=True):
                with gr.Row():
                    tts_preset_files = get_preset_configs("tts")
                    tts_preset_dropdown = gr.Dropdown(
                        choices=tts_preset_files,
                        label="预设配置文件",
                        scale=2
                    )
                    with gr.Column():
                        tts_preset_refresh = gr.Button("刷新", variant="primary", size="lg")
                        tts_preset_load = gr.Button("加载预设", variant="primary", size="lg")
                        
                    tts_preset_name = gr.Textbox(label="保存为", scale=2)
                    with gr.Row():
                        tts_preset_save = gr.Button("保存预设", variant="primary", size="md")
                        tts_preset_message = gr.Textbox(label="预设操作结果")
            
            # 其他TTS配置
            tts_type = gr.Radio(
                choices=["gptsovits", "melotts"],
                value=tts_config.get('type', 'gptsovits'),
                label="TTS类型"
            )
            with gr.Row():
                with gr.Column(scale=2):
                    tts_api = gr.Textbox(
                        value=tts_config.get('api_endpoint', ''),
                        label="API端点"
                    )
                    tts_api_key = gr.Textbox(
                        value=tts_config.get('api_key', ''),
                        label="API密钥"
                    )
                with gr.Column(scale=1):
                    tts_api_test_bt = gr.Button("测试", variant="primary", size="lg")
                    tts_api_output = gr.Textbox(
                        label="测试输出",
                        lines=1,
                        max_lines=1,
                        autoscroll=True
                    )
                
            with gr.Accordion("请求配置", open=True):
                mode = gr.Radio(
                    choices=["基础模式", "高级模式"],
                    value="基础模式",
                    label="配置模式"
                )
                
                with gr.Group(visible=True) as basic_config_group:
                    with gr.Group(visible=True if tts_type.value == "gptsovits" else False) as gptsovits_group:
                        with gr.Row():
                            gptsovits_prompt_lang = gr.Textbox(
                                value=tts_config.get("request_body", {}).get('prompt_lang', 'zh'),
                                label="prompt_lang"
                            )
                            gptsovits_prompt_text = gr.Textbox(
                                value=tts_config.get("request_body", {}).get('prompt_text', '我叫小黑，我也是妖精。'),
                                label="prompt_text"
                        )
                            
                            gptsovits_text_lang = gr.Textbox(
                                value=tts_config.get("request_body", {}).get('text_lang', 'zh'),
                                label="text_lang"
                            )
                            gptsovits_ref_audio_path = gr.Textbox(
                                value=tts_config.get("request_body", {}).get('ref_audio_path', 'Voice/boy_refer.wav'),
                                label="ref_audio_path"
                            )
                            
                        with gr.Row():
                            gptsovits_batch_size = gr.Slider(
                                value=tts_config.get("request_body", {}).get('batch_size', 8),
                                minimum=1,
                                maximum=16,
                                step=1,
                                label="batch_size",
                                scale=2
                            )
                            with gr.Column():
                                gptsovits_split_bucket = gr.Checkbox(
                                    value=tts_config.get("request_body", {}).get('split_bucket', False),
                                    label="split_bucket"
                                )
                                gptsovits_parallel_infer = gr.Checkbox(
                                    value=tts_config.get("request_body", {}).get('parallel_infer', True),
                                    label="parallel_infer"
                                )
                            
                    with gr.Group(visible=True if tts_type.value == "melotts" else False) as melotts_group:
                        with gr.Row():
                            melotts_language = gr.Textbox(
                                value=tts_config.get("request_body", {}).get('language', 'default'),
                                label="language"
                            )
                            melotts_speaker = gr.Textbox(
                                value=tts_config.get("request_body", {}).get('speaker', 'ZH_MIX_EN-default.wav'),
                                label="speaker"
                            )
                            melotts_speed = gr.Slider(
                                value=tts_config.get("request_body", {}).get('speed', 1.0),
                                minimum=0.5,
                                maximum=2.0,
                                step=0.1,
                                label="speed"
                            )
                    
                with gr.Group(visible=False) as advanced_config_group:
                    tts_request_headers = gr.Code(
                        value=json.dumps(tts_config.get("request_headers", {}), indent=2, ensure_ascii=False),
                        language="json",
                        label="请求头配置(JSON)"
                    )
                    tts_request_body = gr.Code(
                        value=json.dumps(tts_config.get("request_body", {}), indent=2, ensure_ascii=False),
                        language="json",
                        label="请求体配置(JSON)"
                    )
                
                # 绑定配置模式相关事件
                mode.change(
                    fn=lambda x: (gr.Group(visible=x == "基础模式"), gr.Group(visible=x == "高级模式")),
                    inputs=mode,
                    outputs=[basic_config_group, advanced_config_group]
                )
                
                # 绑定TTS类型相关事件
                tts_type.change(
                    fn=lambda x: (gr.Group(visible=x == "gptsovits"), gr.Group(visible=x == "melotts")),
                    inputs=tts_type,
                    outputs=[gptsovits_group, melotts_group]
                )
                
            
            # 绑定TTS预设配置相关事件
            tts_preset_refresh.click(
                fn=lambda: gr.Dropdown(choices=get_preset_configs("tts")),
                outputs=tts_preset_dropdown
            )
            
            # 加载TTS预设配置
            def load_tts_preset(preset_file):
                preset_config, message = load_preset_config("tts", preset_file)
                if preset_config:
                    tts_type = preset_config.get('type', 'gptsovits')
                    api_endpoint = preset_config.get('api_endpoint', '')
                    api_key = preset_config.get('api_key', '')
                    
                    gptsovits_ref_audio_path = preset_config.get('request_body', {}).get('ref_audio_path', '')
                    gptsovits_prompt_lang = preset_config.get('request_body', {}).get('prompt_lang', '')
                    gptsovits_prompt_text = preset_config.get('request_body', {}).get('prompt_text', '')
                    gptsovits_text_lang = preset_config.get('request_body', {}).get('text_lang', '')
                    gptsovits_batch_size = preset_config.get('request_body', {}).get('batch_size', 1)
                    gptsovits_split_bucket = preset_config.get('request_body', {}).get('split_bucket', False)
                    gptsovits_parallel_infer = preset_config.get('request_body', {}).get('parallel_infer', True)
                    
                    melotts_language = preset_config.get('request_body', {}).get('language', 'default')
                    melotts_speaker = preset_config.get('request_body', {}).get('speaker', 'ZH_MIX_EN-default.wav')
                    melotts_speed = preset_config.get('request_body', {}).get('speed', 1.0)
                    
                    header_json = json.dumps(preset_config.get('request_header', {}), indent=2, ensure_ascii=False)
                    body_json = json.dumps(preset_config.get('request_body', {}), indent=2, ensure_ascii=False)
                    
                    return message, tts_type, api_endpoint, api_key, \
                        gptsovits_ref_audio_path, gptsovits_prompt_lang, gptsovits_prompt_text, gptsovits_text_lang, gptsovits_batch_size, gptsovits_split_bucket, gptsovits_parallel_infer, \
                        melotts_language, melotts_speaker, melotts_speed, \
                        header_json, body_json
                return message
            
            tts_preset_load.click(
                fn=load_tts_preset,
                inputs=tts_preset_dropdown,
                outputs=[
                    tts_preset_message, tts_type, tts_api, tts_api_key, 
                    gptsovits_ref_audio_path, gptsovits_prompt_lang, gptsovits_prompt_text, gptsovits_text_lang, gptsovits_batch_size, gptsovits_split_bucket, gptsovits_parallel_infer,
                    melotts_language, melotts_speaker, melotts_speed,
                    tts_request_headers, tts_request_body
                ]
            )
            
            # 保存TTS预设配置
            def save_tts_preset(*args) -> tuple:
                try:
                    config_data = save_config(*args[:-1])
                    result = save_preset_config("tts", config_data, args[-1])
                    return result, gr.Dropdown(choices=get_preset_configs("tts"))
                except json.JSONDecodeError:
                    return "TTS请求体JSON格式错误，配置未保存！", gr.Dropdown()
            
            tts_preset_save.click(
                fn=save_tts_preset,
                inputs=[
                    tts_type, tts_api, mode, tts_api_key,
                    gptsovits_ref_audio_path, gptsovits_prompt_lang, gptsovits_prompt_text, gptsovits_text_lang, gptsovits_batch_size, gptsovits_split_bucket, gptsovits_parallel_infer,
                    melotts_language, melotts_speaker, melotts_speed,
                    tts_request_headers, tts_request_body, tts_preset_name
                ],
                outputs=[tts_preset_message, tts_preset_dropdown]
            )
            
            def tts_api_test() -> str:
                from services.tts import TTS
                tts = TTS()
                success, message = tts.test()
                return message
            
            tts_api_test_bt.click(
                fn=tts_api_test,
                outputs=tts_api_output
            )
    
    return [
        tts_type, tts_api, mode, tts_api_key, 
        gptsovits_ref_audio_path, gptsovits_prompt_lang, gptsovits_prompt_text, gptsovits_text_lang, gptsovits_batch_size, gptsovits_split_bucket, gptsovits_parallel_infer,
        melotts_language, melotts_speaker, melotts_speed,
        tts_request_headers, tts_request_body
    ]


def save_config(tts_type, tts_api, mode, tts_api_key, 
                gptsovits_ref_audio_path, gptsovits_prompt_lang, gptsovits_prompt_text, gptsovits_text_lang, gptsovits_batch_size, gptsovits_split_bucket, gptsovits_parallel_infer,
                melotts_language, melotts_speaker, melotts_speed,
                tts_request_headers, tts_request_body
                ) -> dict:
    
    tts_config = {
        "type": tts_type,
        "api_endpoint": tts_api,
        "api_key": tts_api_key
    }
    
    if mode == "基础模式":
        tts_config["request_headers"] = {}
        
        if tts_type == "gptsovits":
            tts_config["request_body"] = {
                "ref_audio_path": gptsovits_ref_audio_path,
                "prompt_lang": gptsovits_prompt_lang,
                "prompt_text": gptsovits_prompt_text,
                "text_lang": gptsovits_text_lang,
                "batch_size": gptsovits_batch_size,
                "split_bucket": gptsovits_split_bucket,
                "parallel_infer": gptsovits_parallel_infer
            }
        elif tts_type == "melotts":
            tts_config["request_body"] = {
                "language": melotts_language,
                "speaker": melotts_speaker,
                "speed": melotts_speed
            }
    else:
        tts_config["request_headers"] = json.loads(tts_request_headers)
        tts_config["request_body"] = json.loads(tts_request_body)
    
    return tts_config


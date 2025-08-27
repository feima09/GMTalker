import gradio as gr
import json

from utils import config
from .common import get_preset_configs, load_preset_config, save_preset_config


def create_ui() -> list:
    Config = config.Config.get("GPT", {})
    with gr.TabItem("GPT配置"):
        with gr.Group():
            # 预设配置管理
            with gr.Accordion("预设配置管理", open=True):
                with gr.Row():
                    gpt_preset_files = get_preset_configs("gpt")
                    gpt_preset_dropdown = gr.Dropdown(
                        choices=gpt_preset_files,
                        label="预设配置文件",
                        scale=2
                    )
                    with gr.Column():
                        gpt_preset_refresh = gr.Button("刷新", variant="primary", size="lg")
                        gpt_preset_load = gr.Button("加载预设", variant="primary", size="lg")
                    
                    gpt_preset_name = gr.Textbox(label="保存为", scale=2)
                    with gr.Row():
                        gpt_preset_save = gr.Button("保存预设", variant="primary", size="md")
                        gpt_preset_message = gr.Textbox(label="预设操作结果")
            
            # 其他GPT配置
            gpt_type = gr.Radio(
                choices=["openai", "百炼应用"],
                value=Config.get("type", "openai"),
                label="GPT类型"
            )
            
            with gr.Row():
                with gr.Column(scale=2):
                    gpt_api = gr.Textbox(
                        value=Config.get("api_endpoint", ""),
                        label="API URL"
                    )
                    gpt_api_key = gr.Textbox(
                        value=Config.get("api_key", ''),
                        label="API密钥"
                    )
                with gr.Column(scale=1):
                    gpt_api_test_bt = gr.Button("测试", variant="primary", size="lg")
                    gpt_api_output = gr.Textbox(
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
            
                with gr.Group() as basic_config_group:
                    with gr.Group(visible=True if gpt_type.value == "openai" else False) as openai_config_group:
                        gpt_model = gr.Textbox(
                            value=Config.get("request_body", {}).get("model", "Qwen3-8B"),
                            label="模型名称"
                        )
                            
                        with gr.Row():
                            gpt_max_tokens = gr.Slider(
                                value=Config.get("request_body", {}).get("max_tokens", 512),
                                minimum=256,
                                maximum=131068,
                                step=1,
                                label="max_tokens"
                            ) 
                            gpt_temperature = gr.Slider(
                                value=Config.get("request_body", {}).get("temperature", 0.7),
                                minimum=0.0,
                                maximum=2.0,
                                step=0.01,
                                label="temperature"
                            )
                            gpt_top_p = gr.Slider(
                                value=Config.get("request_body", {}).get("top_p", 0.8),
                                minimum=0.0,
                                maximum=1.0,
                                step=0.01,
                                label="top_p"
                            )
                            gpt_top_k = gr.Slider(
                                value=Config.get("request_body", {}).get("top_k", 20),
                                minimum=0,
                                maximum=100,
                                step=1,
                                label="top_k"
                            )
                    
                with gr.Group(visible=False) as advanced_config_group:
                    gpt_request_headers = gr.Code(
                        value=json.dumps(Config.get("request_headers", {}), indent=2, ensure_ascii=False),
                        language="json",
                        label="请求头配置(JSON)"
                    )
                    
                    gpt_request_body = gr.Code(
                        value=json.dumps(Config.get("request_body", {}), indent=2, ensure_ascii=False),
                        language="json",
                        label="请求体配置(JSON)"
                    )
                    
                mode.change(
                    fn=lambda x: (gr.Group(visible=x == "基础模式"), gr.Group(visible=x == "高级模式")),
                    inputs=mode,
                    outputs=[basic_config_group, advanced_config_group]
                )
            
            with gr.Accordion("RAG配置") as rag_accordion:
                rag_config = Config.get("RAG", {})
                
                rag_enable = gr.Checkbox(
                    value=rag_config.get("enable", False),
                    label="启用RAG"
                )
                
                with gr.Group(visible=rag_enable.value) as rag_group:
                    with gr.Row():
                        embedding_config = rag_config.get("embedding", {})
                        
                        embedding_api = gr.Textbox(
                            value=embedding_config.get("api_endpoint", ""),
                            label="Embedding API端点"
                        )
                        embedding_model = gr.Textbox(
                            value=embedding_config.get("model", ""),
                            label="Embedding模型"
                        )
                        embedding_api_key = gr.Textbox(
                            value=embedding_config.get("api_key", "empty"),
                            type="password",
                            label="API密钥"
                        )
                        rag_top_k = gr.Slider(
                            value=rag_config.get("top_k", 3),
                            minimum=1,
                            maximum=10,
                            step=1,
                            label="检索数量"
                        )
                
                rag_enable.change(
                    fn=lambda x: gr.Group(visible=x),
                    inputs=rag_enable,
                    outputs=rag_group
                )
            
            # 绑定GPT类型相关事件
            gpt_type.change(
                fn=lambda x: (gr.Group(visible=True if x == "openai" else False), gr.Accordion(visible=False if x == "百炼应用" else True)),
                inputs=gpt_type,
                outputs=[openai_config_group, rag_accordion]
            )
            
            # 绑定GPT预设配置相关事件
            gpt_preset_refresh.click(
                fn=lambda: gr.Dropdown(choices=get_preset_configs("gpt")),
                outputs=gpt_preset_dropdown
            )
            
            # 加载GPT预设配置
            def load_gpt_preset(preset_file) -> tuple:
                preset_config, message = load_preset_config("gpt", preset_file)
                if preset_config:
                    gpt_type = preset_config.get('type', 'openai')
                    api_endpoint = preset_config.get('api_endpoint', '')
                    api_key = preset_config.get('api_key', '')
                    
                    # 请求配置
                    api_model = preset_config.get('request_body', {}).get('model', '')
                    max_tokens = preset_config.get('request_body', {}).get('max_tokens', 512)
                    temperature = preset_config.get('request_body', {}).get('temperature', 0.7)
                    top_p = preset_config.get('request_body', {}).get('top_p', 0.8)
                    top_k = preset_config.get('request_body', {}).get('top_k', 20)
                    headers_json = json.dumps(preset_config.get('request_headers', {}), indent=2, ensure_ascii=False)
                    body_json = json.dumps(preset_config.get('request_body', {}), indent=2, ensure_ascii=False)
                    
                    # RAG配置
                    rag_config = preset_config.get('RAG', {})
                    rag_enable = rag_config.get('enable', False)
                    embedding_config = rag_config.get('embedding', {})
                    embedding_api = embedding_config.get('api_endpoint', '')
                    embedding_model = embedding_config.get('model', '')
                    embedding_api_key = embedding_config.get('api_key', '')
                    rag_top_k = rag_config.get('top_k', 3)
                    
                    return gpt_type, api_endpoint, api_key, api_model, max_tokens, temperature, top_p, top_k, headers_json, \
                            body_json, rag_enable, embedding_api, embedding_model, embedding_api_key, rag_top_k, message
                return None, None, None, None, None, None, None, None, None, None, None, None, None, None, message
            
            gpt_preset_load.click(
                fn=load_gpt_preset,
                inputs=gpt_preset_dropdown,
                outputs=[gpt_type, gpt_api, gpt_api_key, gpt_model, gpt_max_tokens, gpt_temperature, gpt_top_p, gpt_top_k,
                         gpt_request_headers, gpt_request_body, rag_enable, embedding_api, embedding_model,
                         embedding_api_key, rag_top_k, gpt_preset_message]
            )
            
            # 保存GPT预设配置
            def save_gpt_preset(*args) -> tuple:
                try:
                    config_data = save_config(*args[:-1])
                    result = save_preset_config("gpt", config_data, args[-1])
                    return result, gr.Dropdown(choices=get_preset_configs("gpt"))
                except json.JSONDecodeError:
                    return "GPT请求体JSON格式错误，配置未保存！", gr.Dropdown()
            
            gpt_preset_save.click(
                fn=save_gpt_preset,
                inputs=[gpt_type, gpt_api, mode, gpt_model, gpt_api_key, gpt_max_tokens, gpt_temperature,
                        gpt_top_p, gpt_top_k, gpt_request_headers, gpt_request_body, rag_enable,
                        embedding_api, embedding_model, embedding_api_key, rag_top_k, gpt_preset_name],
                outputs=[gpt_preset_message, gpt_preset_dropdown]
            )
            
            # 测试GPT API
            def gpt_api_test() -> str:
                from services.gpt import GPT
                gpt = GPT()
                suceess, message = gpt.test()
                return message
            
            gpt_api_test_bt.click(
                fn=gpt_api_test,
                outputs=gpt_api_output
            )
            
    return [
        gpt_type, gpt_api, mode, gpt_model, gpt_api_key, gpt_max_tokens, gpt_temperature,
        gpt_top_p, gpt_top_k, gpt_request_headers, gpt_request_body, rag_enable,
        embedding_api, embedding_model, embedding_api_key, rag_top_k
    ]
                    

def save_config(gpt_type, gpt_api, mode, gpt_model, gpt_api_key, gpt_max_tokens, gpt_temperature,
                gpt_top_p, gpt_top_k, gpt_request_headers, gpt_request_body, rag_enable,
                embedding_api, embedding_model, embedding_api_key, rag_top_k) -> dict:
    gpt_config = {
        "type": gpt_type,
        "api_endpoint": gpt_api,
        "api_key": gpt_api_key,
        "RAG": {
            "enable": rag_enable,
            "embedding": {
                "api_endpoint": embedding_api,
                "model": embedding_model,
                "api_key": embedding_api_key
            },
            "top_k": int(rag_top_k)
        }
    }
    
    if mode == "基础模式":
        gpt_config["request_headers"] = {}
        if gpt_type == "openai":
            gpt_config["request_body"] = {
                "model": gpt_model,
                "max_tokens": int(gpt_max_tokens),
                "temperature": float(gpt_temperature),
                "top_p": float(gpt_top_p),
                "top_k": int(gpt_top_k)
            }
        elif gpt_type == "百炼应用":
            gpt_config["request_body"] = {
                "parameters":  {},
                "debug": {}
            }
            gpt_config.update({
                "RAG": {
                    "enable": False
                }
            })
            
    else:
        gpt_config["request_headers"] = json.loads(gpt_request_headers)
        gpt_config["request_body"] = json.loads(gpt_request_body)
    
    return gpt_config

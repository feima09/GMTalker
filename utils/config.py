import os
import yaml
import json

home_dir = os.getcwd()

Config = {}
Prompt = ""
Template = ""
Webui = {}
Hotword_msg = ""

default_config = {
    "log_level": "INFO",
    "host": "127.0.0.1",
    "port": 5002,
    "GPT": {
        "type": "openai",
        "api_endpoint": "https://api.openai.com/v1/chat/completions",
        "api_key": "empty",
        "request_headers": {},
        "request_body": {
            "model": "gpt-4.1",
            "max_tokens": 4096,
            "temperature": 1.0,
            "top_p": 1.0,
            "top_k": 0,
            "min_p": 0,
        },
        "RAG": {
            "enable": False,
            "embedding": {
                "api_endpoint": "https://api.openai.com/v1/embeddings",
                "api_key": "empty",
                "model": "text-embedding-ada-002"
            },
            "top_k": 3
        },
    },
    "TTS": {
        "type": "gptsovits",
        "api_endpoint": "http://127.0.0.1:9880/tts",
        "api_key": "empty",
        "request_headers": {},
        "request_body": {
            "ref_audio_path": "Voice/boy_refer.wav",
            "prompt_text": "我叫小黑，我也是妖精。",
            "prompt_lang": "zh",
            "text_lang": "zh",
            "batch_size": 8,
            "split_bucket": False,
            "parallel_infer": True
        }
    },
    "ASR": {
        "enable": False,
        "url": "ws://127.0.0.1:10096",
        "mode": "wake",
        "wake_words": "光小明,你好,在吗",
        "timeout": 1.0,
        "interrupt": False
    },
    "Player": {
        "mode": "local",
        "Audio2Face": {
            "url": "127.0.0.1:50051",
            "player": "/World/audio2face/audio_player_streaming"
        }
    }
}

default_prompt = """
【你的身份】\\n
你叫光小明，是由光明实验室自主研发的法务智能助手。\\n
你被设计为具有广泛的知识和能力，拥有广泛的法律知识和严格的信息处理能力，能够为用户提供准确可靠的法律信息和服务。\\n\\n

【你的目标】\\n
你的目标是帮助人们解决法律疑问，并引导他们合法合规地行事，为用户提供各种帮助和服务。\\n\\n

【当前情景】\\n
你现在处于一个法律咨询的场景中，用户可能会询问有关法律问题、法规、合同、诉讼等方面的内容。\\n
你的回答必须符合与人正常的口头交流，不能使用任何Mardown格式等，只需要纯文字生成即可。\\n\\n
"""

default_template = """
你是一个智能问答助手。请根据下面提供的“相关问答信息”来回答用户的“用户问题”。
请仔细阅读并理解相关问答信息。
如果相关信息中没有能直接回答用户问题的答案，请明确告知用户“根据提供的信息，我无法回答这个问题”。
不要编造信息。回答应简洁、准确，并使用中文。

相关问答信息:
{context}

用户问题:
{question}

回答:
"""

default_webui = {
    "audio2face": {
        "enable": False,
        "path": "",
        "usd_path": ""
    },
    "ue5": {
        "enable": False,
        "path": ""
    }
}

default_hotword = """
光小明 20
"""


def load_hotwords(file_path) -> str:
    fst_dict = {}
    hotword_msg = ""
    if file_path.strip() != "":
        try:
            f_scp = open(file_path, 'r', encoding='utf-8')
        except FileNotFoundError:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(default_hotword)
            f_scp = open(file_path, 'r', encoding='utf-8')
        finally:
            hot_lines = f_scp.readlines()
            for line in hot_lines:
                words = line.strip().split(" ")
                if len(words) < 2:
                    continue
                try:
                    fst_dict[" ".join(words[:-1])] = int(words[-1])
                except ValueError:
                    pass
            hotword_msg = json.dumps(fst_dict)
    return hotword_msg


def reload_config() -> None:
    """
    重新加载配置文件
    """
    global Config, Prompt, Template, Webui, Hotword_msg
    try:
        with open(f"{home_dir}/configs/config.yaml", 'r', encoding='utf-8') as file:
            Config = yaml.safe_load(file)
    except FileNotFoundError:
        Config = default_config
        with open(f"{home_dir}/configs/config.yaml", 'w', encoding='utf-8') as file:
            yaml.safe_dump(Config, file, allow_unicode=True)

    try:
        with open(f"{os.getcwd()}/configs/prompt.txt", 'r', encoding='utf-8') as file:
            Prompt = file.read()
    except FileNotFoundError:
        Prompt = default_prompt
        with open(f"{os.getcwd()}/configs/prompt.txt", 'w', encoding='utf-8') as file:
            file.write(Prompt)
        
    try:
        with open(os.path.join(home_dir, "configs", "rag", "template.txt"), 'r', encoding='utf-8') as file:
            Template = file.read()
    except FileNotFoundError:
        Template = default_prompt
        with open(os.path.join(home_dir, "configs", "rag", "template.txt"), 'w', encoding='utf-8') as file:
            file.write(Template)

    try:
        with open(f"{home_dir}/configs/webui.yaml", 'r', encoding='utf-8') as file:
            Webui = yaml.safe_load(file)
    except FileNotFoundError:
        Webui = default_webui
        with open(f"{home_dir}/configs/webui.yaml", 'w', encoding='utf-8') as file:
            yaml.safe_dump(Webui, file, allow_unicode=True)

    Hotword_msg = load_hotwords(f"{home_dir}/configs/hotword.txt")


reload_config()


def save_config(config: dict, filename: str) -> None:
    """
    保存配置到文件
    
    Args:
        config (dict): 要保存的配置字典
        filename (str): 配置文件名
    """
    with open(f"{home_dir}/configs/{filename}", 'w', encoding='utf-8') as file:
        yaml.safe_dump(config, file, allow_unicode=True)
        
    reload_config()
        
from utils import config


def GPT():
    gpt = config.Config.get("GPT", "")
    mode = gpt.get("type", "openai")
    rag_enable = gpt.get("RAG", "").get("enable", False)
    
    if mode == "openai":
        if rag_enable:
            from .rag import RAG
            return RAG()
        else:
            from .openai import OpenAI
            return OpenAI()
    elif mode == "百炼应用":
        from .bailian import Bailian
        return Bailian()
    else:
        raise ValueError(f"Invalid GPT type: {mode}")

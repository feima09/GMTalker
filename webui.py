"""
Webui 入口脚本

启动方法：python webui.py
"""

from webui import webui

if __name__ == "__main__":
    print("正在启动Webui...")
    webui.launch(server_name="0.0.0.0", server_port=7860, share=False, inbrowser=True)

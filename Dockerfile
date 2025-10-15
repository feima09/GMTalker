FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（音频支持和编译工具）
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    alsa-utils \
    pulseaudio \
    portaudio19-dev \
    python3-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口（根据您的 webui 实际端口调整）
EXPOSE 5002
EXPOSE 7860

# 启动命令
CMD ["python3", "webui.py"]

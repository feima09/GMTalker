# 设置控制台编码为UTF-8，解决中文乱码问题
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

.\python\python.exe -m pip config set global.index-url https://pypi.org/simple
# .\python\python.exe -m pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

.\python\python.exe -m pip install --upgrade pip
.\python\python.exe -m pip install -r requirements.txt

Start-Sleep -Seconds 3

# 设置Python环境变量，确保中文输出正常
$env:PYTHONIOENCODING = "utf-8"

.\python\python.exe webui.py

Read-Host -Prompt "Press Enter to exit"

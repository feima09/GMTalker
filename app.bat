@echo off

chcp 65001 >nul
set PYTHONIOENCODING=utf-8

if not exist ".venv" (
    python\python.exe -m virtualenv .venv

    @REM .venv\Scripts\python.exe -m pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
    @REM .venv\Scripts\python.exe -m pip config set global.index-url https://pypi.org/simple

    call .venv\Scripts\activate

    python -m pip install --upgrade pip setuptools
    pip install -r requirements.txt

    ping 127.0.0.1 -n 3 >nul

) else (
    call .venv\Scripts\activate
)

python app.py 2>&1

@pause

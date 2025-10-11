#!/bin/bash

export PYTHONIOENCODING=utf-8
export LANG=zh_CN.UTF-8

if [ ! -d ".venv" ]; then
    python3 -m venv .venv

    # .venv/bin/python -m pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
    # .venv/bin/python -m pip config set global.index-url https://pypi.org/simple

    source .venv/bin/activate

    python -m pip install --upgrade pip setuptools
    pip install -r requirements.txt

    sleep 3

else
    source .venv/bin/activate
fi

python app.py 2>&1

read -p "Press Enter to continue..."

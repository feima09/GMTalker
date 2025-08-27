[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null
$env:PYTHONIOENCODING = "utf-8"

if (-not (Test-Path -Path ".\.venv")) {
    .\python\python.exe -m virtualenv .venv

    # .\.venv\Scripts\python.exe -m pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
    # .\.venv\Scripts\python.exe -m pip config set global.index-url https://pypi.org/simple

    .\.venv\Scripts\activate

    python -m pip install --upgrade pip setuptools
    pip install -r requirements.txt

    Start-Sleep -Seconds 3

} else {
    .\.venv\Scripts\activate
}

python app.py

Read-Host -Prompt "Press Enter to exit"

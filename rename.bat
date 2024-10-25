@echo off

chcp 65001

echo 環境構築を開始します...

REM venv が存在する場合はスキップ
if not exist .venv\Scripts\activate.bat (
  python -m venv .venv
)
call .venv\Scripts\activate.bat

echo 環境構築が完了しました。

echo 必要なライブラリの準備を行っています...

REM requirements.txt 内のパッケージを個別にインストール有無を確認
for /f %%i in (requirements.txt) do (
  pip show %%i > nul 2>&1
  if errorlevel 1 (
    echo %%i をインストールしています...
    pip install %%i
  ) else (
    echo %%i は既にインストールされています。
  )
)

echo ライブラリの準備が完了しました。

echo rename.py を実行します...

python rename.py

echo rename.py の実行が完了しました。

pause
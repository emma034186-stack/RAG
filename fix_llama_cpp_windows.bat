
@echo off
setlocal

REM Python 安裝路徑（Python 3.10）
set PY310_PATH=%LocalAppData%\Programs\Python\Python310
set TARGET_DIR=%PY310_PATH%\Lib\site-packages\llama_cpp\lib

echo [🛠] 建立目標資料夾：%TARGET_DIR%
mkdir "%TARGET_DIR%" >nul 2>&1

echo [⬇️ ] 正在下載 llama.dll（AVX2 版本）...
curl -L -o "%TARGET_DIR%\llama.dll" https://huggingface.co/ggerganov/llama.cpp/resolve/main/build/bin/Release/llama.dll

if exist "%TARGET_DIR%\llama.dll" (
    echo [✅] 已成功下載並放置 llama.dll！
) else (
    echo [❌] 下載失敗，請手動下載並放入：%TARGET_DIR%
)

pause

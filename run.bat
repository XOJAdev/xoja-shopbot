@echo off
echo 🚀 Telegram Donat Bot ishga tushirilmoqda...

REM Virtual muhitni tekshirish
if not exist "venv" (
    echo 📦 Virtual muhit yaratilmoqda...
    python -m venv venv
)

REM Virtual muhitni faollashtirish
echo ✅ Virtual muhit faollashtirilmoqda...
call venv\Scripts\activate.bat

REM Kutubxonalarni o'rnatish
echo 📚 Kutubxonalar o'rnatilmoqda...
pip install -r requirements.txt

REM Botni ishga tushirish
echo 🤖 Bot ishga tushmoqda...
python bot.py

pause

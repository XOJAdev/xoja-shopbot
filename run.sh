#!/bin/bash

echo "🚀 Telegram Donat Bot ishga tushirilmoqda..."

# Virtual muhitni tekshirish
if [ ! -d "venv" ]; then
    echo "📦 Virtual muhit yaratilmoqda..."
    python3 -m venv venv
fi

# Virtual muhitni faollashtirish
echo "✅ Virtual muhit faollashtirilmoqda..."
source venv/bin/activate

# Kutubxonalarni o'rnatish
echo "📚 Kutubxonalar o'rnatilmoqda..."
pip install -r requirements.txt

# Botni ishga tushirish
echo "🤖 Bot ishga tushmoqda..."
python bot.py

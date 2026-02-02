# 🚀 TEZKOR O'RNATISH QO'LLANMASI

## 📋 1-QADAM: Telegram Bot yaratish

1. Telegram'da @BotFather botini oching
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: My Donat Bot)
4. Bot username'ini kiriting (masalan: my_donat_bot)
5. Token oling (masalan: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)

## 📋 2-QADAM: O'z User ID'ni bilish

1. Telegram'da @userinfobot ni oching
2. `/start` yuboring
3. Sizning ID raqamingiz ko'rsatiladi (masalan: 123456789)

## 📋 3-QADAM: Loyihani sozlash

### A. Config.py faylini tahrirlash

`config.py` faylini oching va quyidagilarni o'zgartiring:

```python
# 1. Bot tokenini kiriting (@BotFather dan)
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# 2. O'z ID raqamingizni kiriting
ADMIN_IDS = [123456789]

# 3. To'lov kartasi raqamini kiriting
CARD_NUMBER = "8600 1234 5678 9012"

# 4. Qo'llab-quvvatlash username'ini kiriting
SUPPORT_USERNAME = "support"
```

### B. Bot.py faylini tahrirlash

`bot.py` faylining 19-qatorida:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Buni config.py dan import qiling
```

O'rniga:

```python
from config import BOT_TOKEN
```

## 📋 4-QADAM: Kutubxonalarni o'rnatish

### Windows:
```cmd
run.bat
```

### Linux/Mac:
```bash
chmod +x run.sh
./run.sh
```

### Qo'lda o'rnatish:
```bash
# Virtual muhit yaratish
python -m venv venv

# Virtual muhitni faollashtirish
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt
```

## 📋 5-QADAM: O'zingizni admin qilish

Bot ishga tushgandan so'ng:

### Usul 1: Python orqali
```python
from database.db import Database
db = Database()
db.set_admin(123456789, True)  # O'z ID raqamingizni kiriting
```

### Usul 2: Bot orqali
1. Botni ishga tushiring
2. Telegram'da botga `/start` yuboring
3. Python shell'da yuqoridagi kodni ishga tushiring
4. Telegram'da `/admin` yuboring

## 📋 6-QADAM: Botni ishga tushirish

```bash
python bot.py
```

## ✅ Tayyor!

Endi botingiz to'liq ishga tayyor! 

### Test qilish:
1. Telegram'da botingizni oching
2. `/start` buyrug'ini yuboring
3. Tilni tanlang
4. "🎮 Donat qilish" tugmasini bosing
5. O'yinni tanlang va buyurtma bering

### Admin panel:
1. `/admin` buyrug'ini yuboring
2. Admin panelni ko'rasiz

## ⚠️ Muhim!

1. ✅ Bot tokenini hech kimga ko'rsatmang
2. ✅ Admin ID to'g'ri ekanligini tekshiring
3. ✅ Checks papkasi mavjud ekanligini tekshiring
4. ✅ Internet aloqasi borligini tekshiring

## 🆘 Yordam kerakmi?

Agar muammo bo'lsa:
1. README.md faylini o'qing
2. Log'larni ko'rib chiqing
3. Tokenni qayta tekshiring
4. Kutubxonalar o'rnatilganligini tekshiring

## 📞 Qo'llab-quvvatlash

Savollar bo'lsa:
- Telegram: @your_support
- GitHub: Create an issue

Omad! 🎉

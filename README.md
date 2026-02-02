# 🎮 Telegram Donat Bot

Professional telegram bot o'yinlar uchun donat qilish xizmatini ko'rsatish uchun.

## ✨ Xususiyatlar

- 🌐 **3 ta til**: O'zbek, Rus, Ingliz
- 🎮 **4 ta o'yin**: PUBG Mobile, Telegram Premium, Telegram Stars, Mobile Legends
- 💳 **Yarim avtomatik to'lov**: Karta orqali to'lov va chek yuklash
- 👨‍💼 **To'liq admin panel**: Buyurtmalarni boshqarish, narxlar, statistika
- 📊 **Statistika**: Kunlik, oylik, umumiy statistika
- 📢 **Broadcast**: Barcha foydalanuvchilarga xabar yuborish
- 💰 **Narxlarni boshqarish**: Admin panel orqali narxlarni o'zgartirish

## 📋 O'rnatish

### 1. Talablar

```bash
Python 3.8+
pip
```

### 2. Loyihani yuklab olish

```bash
# Git orqali
git clone <repository-url>
cd donat_bot

# Yoki ZIP faylni yuklab olib, unzip qiling
```

### 3. Virtual muhit yaratish (tavsiya etiladi)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 5. Bot sozlamalari

#### A. Config.py orqali (sodda usul)

`config.py` faylini oching va quyidagilarni o'zgartiring:

```python
BOT_TOKEN = "your_bot_token_here"  # @BotFather dan token
ADMIN_IDS = [123456789]  # O'z user ID raqamingiz
CARD_NUMBER = "8600 1234 5678 9012"  # To'lov kartasi
SUPPORT_USERNAME = "support"  # Qo'llab-quvvatlash username
```

#### B. .env fayli orqali (xavfsizroq)

```bash
# .env.example faylini nusxalash
cp .env.example .env

# .env faylini tahrirlash
nano .env
```

### 6. Admin qilish

Botni ishga tushirgandan so'ng, o'zingizni admin qilish uchun:

```python
# Python shell'da
from database.db import Database
db = Database()
db.set_admin(YOUR_USER_ID, True)
```

## 🚀 Ishga tushirish

```bash
python bot.py
```

Bot ishga tushgach, Telegram'da botingizni oching va `/start` buyrug'ini yuboring.

## 📁 Loyiha tuzilmasi

```
donat_bot/
│
├── bot.py                 # Asosiy bot fayli
├── config.py              # Sozlamalar
├── requirements.txt       # Python kutubxonalari
│
├── handlers/              # Bot handlerlari
│   ├── user.py           # Foydalanuvchi handlerlari
│   └── admin.py          # Admin handlerlari
│
├── keyboards/             # Klaviaturalar
│   └── keyboards.py
│
├── database/              # Ma'lumotlar bazasi
│   └── db.py
│
├── languages/             # Tillar
│   ├── uz.json           # O'zbek tili
│   ├── ru.json           # Rus tili
│   └── en.json           # Ingliz tili
│
├── utils/                 # Yordamchi funksiyalar
│   └── helpers.py
│
└── checks/                # Cheklar saqlanadigan papka
```

## 🎯 Foydalanish

### Foydalanuvchi uchun:

1. `/start` - Botni ishga tushirish
2. Tilni tanlash
3. "🎮 Donat qilish" tugmasini bosish
4. O'yinni tanlash
5. Miqdorni tanlash
6. O'yin ID ni kiritish
7. To'lov qilish va chekni yuborish
8. Natijani kutish

### Admin uchun:

1. `/admin` - Admin panelni ochish
2. Yangi buyurtmalarni ko'rish
3. Buyurtmani tasdiqlash/rad etish
4. Narxlarni boshqarish
5. Foydalanuvchilarni ko'rish
6. Statistikani ko'rish
7. Xabar yuborish (broadcast)

## ⚙️ Sozlamalar

### Yangi o'yin qo'shish

`database/db.py` faylida `init_default_prices` funksiyasiga yangi o'yin qo'shing:

```python
('Yangi O\'yin', '100 coin', 10000),
```

### Narxlarni o'zgartirish

Admin panel orqali: `/admin` → "💰 Narxlarni boshqarish"

### Karta raqamini o'zgartirish

`config.py` faylida `CARD_NUMBER` ni o'zgartiring yoki admin orqali:

```python
from database.db import Database
db = Database()
db.set_setting('card_number', '8600 9876 5432 1098')
```

## 📊 Ma'lumotlar bazasi

Bot SQLite dan foydalanadi. Ma'lumotlar bazasi avtomatik yaratiladi.

### Jadvallar:

- `users` - Foydalanuvchilar
- `orders` - Buyurtmalar
- `prices` - Narxlar
- `settings` - Sozlamalar

### Backup olish:

```bash
cp donat_bot.db donat_bot_backup.db
```

## 🔧 Xatoliklarni tuzatish

### Bot ishlamayapti?

1. Token to'g'ri ekanligini tekshiring
2. Internet aloqasini tekshiring
3. Python versiyasini tekshiring (3.8+)
4. Kutubxonalar o'rnatilganligini tekshiring

### Buyurtmalar kelmayapti?

1. Admin ID to'g'ri ekanligini tekshiring
2. `checks/` papka mavjudligini tekshiring
3. Log'larni ko'rib chiqing

### Chek yuklanmayapti?

`checks/` papkasiga yozish huquqi borligini tekshiring:

```bash
chmod 755 checks/
```

## 📝 Litsenziya

Bu loyiha ochiq kodli va o'zingizning ehtiyojlaringizga moslashtira olasiz.

## 🤝 Qo'llab-quvvatlash

Savollar yoki muammolar bo'lsa:
- Issue yarating
- Pull request yuboring
- Telegram: @your_support

## 📈 Yangilanishlar

### v1.0.0 (Joriy versiya)
- ✅ Asosiy funksiyalar
- ✅ 3 til
- ✅ 4 ta o'yin
- ✅ Admin panel
- ✅ Statistika

### Kelgusi yangilanishlar:
- [ ] Avtomatik to'lov (Click, Payme)
- [ ] Ko'proq o'yinlar
- [ ] Referral tizimi
- [ ] Chegirmalar tizimi

## ⚠️ Muhim eslatmalar

1. **Bot tokenini hech kimga ko'rsatmang!**
2. Admin ID raqamlarini to'g'ri kiriting
3. Muntazam ravishda backup oling
4. Log'larni tekshirib turing
5. To'lov ma'lumotlarini xavfsiz saqlang

## 🎉 Tayyor!

Botingiz ishga tayyor! Omad tilaymiz! 🚀

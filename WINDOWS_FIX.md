# 🔧 WINDOWS UCHUN TUZATISH QO'LLANMASI

## ❌ Xatolik sababi
Import yo'lida muammo bo'lgan. Men uni tuzatdim!

---

## ✅ TUZATISH - 2 TA USUL

### **USUL 1: Yangi faylni yuklab olish (OSON)**

1. ❌ Eski `donat_bot` papkasini o'chiring
2. ✅ Yangi yuklab olingan `telegram_donat_bot_fixed.zip` faylni oching
3. ✅ `donat_bot` papkasini Desktop'ga ko'chiring
4. ✅ `config.py` faylini yana tahrirlang (token, admin ID, karta)
5. ✅ `run.bat` faylni ishga tushiring

---

### **USUL 2: Faqat bot.py faylini tuzatish (TEZROQ)**

Agar `config.py` faylni allaqachon to'g'ri sozlagan bo'lsangiz:

#### Qadam 1: bot.py faylini oching
```
C:\Users\asus\Desktop\donat_bot\bot.py
```
Faylni **Notepad** yoki **Notepad++** da oching

#### Qadam 2: 6-7 qatorlarni toping:
Eski kod:
```python
from handlers import user, admin
from database.db import Database
```

#### Qadam 3: O'zgartiring:
Yangi kod:
```python
from handlers.user import router as user_router
from handlers.admin import router as admin_router
from database.db import Database
```

#### Qadam 4: 48-49 qatorlarni toping:
Eski kod:
```python
dp.include_router(user.router)
dp.include_router(admin.router)
```

#### Qadam 5: O'zgartiring:
Yangi kod:
```python
dp.include_router(user_router)
dp.include_router(admin_router)
```

#### Qadam 6: Saqlang
**Ctrl + S** bosing

#### Qadam 7: Botni qayta ishga tushiring
```cmd
cd C:\Users\asus\Desktop\donat_bot
python bot.py
```

---

## 🚀 WINDOWS UCHUN TO'LIQ ISHGA TUSHIRISH

### 1. Config.py ni tekshiring:
```
C:\Users\asus\Desktop\donat_bot\config.py
```

Quyidagilar to'g'ri kiritilganligini tekshiring:
- ✅ BOT_TOKEN
- ✅ ADMIN_IDS (sizning ID raqamingiz)
- ✅ CARD_NUMBER
- ✅ SUPPORT_USERNAME

### 2. CMD ni oching:
- **Windows tugmasini** bosing
- **cmd** deb yozing
- **Enter** bosing

### 3. Papkaga o'ting:
```cmd
cd C:\Users\asus\Desktop\donat_bot
```

### 4. Virtual muhit yarating (birinchi marta):
```cmd
python -m venv venv
```

### 5. Virtual muhitni faollashtiring:
```cmd
venv\Scripts\activate
```

Terminal'da `(venv)` yozilishi kerak:
```
(venv) C:\Users\asus\Desktop\donat_bot>
```

### 6. Kutubxonalarni o'rnating:
```cmd
pip install -r requirements.txt
```

Kutib turing (1-2 daqiqa)...

### 7. Botni ishga tushiring:
```cmd
python bot.py
```

### ✅ Agar:
```
Ma'lumotlar bazasi tayyor
Bot ishga tushdi!
Adminlar: [123456789]
```
Ko'rsatilsa - **TAYYOR!** ✅

---

## 🎯 TELEGRAM'DA TEST QILISH

1. Telegram'ni oching
2. Botingizni toping (@your_bot_username)
3. **/start** yuboring
4. ✅ Til tanlash menyusi chiqishi kerak!

---

## ⚠️ YANA XATOLIK BO'LSA?

### Xato: "No module named 'aiogram'"
**Yechim:**
```cmd
pip install aiogram==3.13.1
```

### Xato: "config module not found"
**Yechim:**
`config.py` fayli `donat_bot` papkasida borligini tekshiring

### Xato: Token invalid
**Yechim:**
1. @BotFather ga boring
2. `/mybots` yuboring
3. Botingizni tanlang
4. **API Token** bosing
5. Tokenni ko'chirib, `config.py` ga qo'ying

---

## 💡 FOYDALI MASLAHATLAR

### Virtual muhitni yopish:
```cmd
deactivate
```

### Botni to'xtatish:
**Ctrl + C** bosing CMD da

### Botni fonda ishlatish:
1. CMD ni **minimizatsiya** qiling (yopmang!)
2. Bot ishlayveradi
3. CMD ni yopsangiz, bot to'xtaydi

---

## 📞 YORDAM

Agar hali ham ishlamasa:

1. CMD'dagi **BARCHASINI** screenshot qiling
2. `config.py` faylini screenshot qiling (token'ni yashiring!)
3. Qaysi qismda to'xtab qolganini ayting

Omad! 🚀

"""
Bot sozlamalari

Bu faylda botni ishga tushirish uchun zarur sozlamalar mavjud.
"""

import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# ========================================
# BOT TOKEN (Majburiy!)
# ========================================
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ========================================
# ADMIN USER ID (Majburiy!)
# ========================================
# Bir nechta admin ID larni vergul bilan .env ichiga yozasiz
admin_ids_str = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(i) for i in admin_ids_str.split(",") if i.strip().isdigit()]

# ========================================
# TO'LOV SOZLAMALARI
# ========================================
CARD_NUMBER = os.getenv("CARD_NUMBER")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME")

# ========================================
# DATABASE
# ========================================
DB_PATH = "donat_bot.db"

# ========================================
# FAYLLAR
# ========================================
CHECKS_FOLDER = "checks"

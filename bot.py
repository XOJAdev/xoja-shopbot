import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.user import router as user_router
from handlers.admin import router as admin_router
from database.db import Database
import config

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Bot tokenini config.py dan olamiz
BOT_TOKEN = config.BOT_TOKEN


async def main():
    """Asosiy funksiya"""
    # Database yaratish
    db = Database()
    logger.info("Ma'lumotlar bazasi tayyor")
    
    # Adminlarni avtomatik qo'shish
    for admin_id in config.ADMIN_IDS:
        if not db.is_admin(admin_id):
            # Agar user mavjud bo'lsa, admin qilish
            user = db.get_user(admin_id)
            if user:
                db.set_admin(admin_id, True)
                logger.info(f"Admin qo'shildi: {admin_id}")
    
    # Sozlamalarni yangilash
    db.set_setting('card_number', config.CARD_NUMBER)
    db.set_setting('support_username', config.SUPPORT_USERNAME)
    
    # Bot va Dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Routerlarni qo'shish
    dp.include_router(user_router)
    dp.include_router(admin_router)
    
    logger.info("Bot ishga tushdi!")
    logger.info(f"Adminlar: {config.ADMIN_IDS}")
    
    try:
        # Polling boshlash
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi")

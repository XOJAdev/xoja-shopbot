from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from utils.helpers import translator
from database.db import Database


db = Database()


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🇺🇿 O'zbek", callback_data="lang_uz")
    builder.button(text="🇷🇺 Русский", callback_data="lang_ru")
    builder.button(text="🇬🇧 English", callback_data="lang_en")
    
    builder.adjust(1)
    return builder.as_markup()


def get_main_menu(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text=translator.get('select_language', language))
    builder.button(text=translator.get('make_donation', language))
    builder.button(text=translator.get('my_orders', language))
    builder.button(text=translator.get('help', language))
    
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


def get_games_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """O'yinlarni tanlash klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=translator.get('pubg_mobile', language),
        callback_data="game_pubg"
    )
    builder.button(
        text=translator.get('telegram_premium', language),
        callback_data="game_telegram_premium"
    )
    builder.button(
        text=translator.get('telegram_stars', language),
        callback_data="game_telegram_stars"
    )
    builder.button(
        text=translator.get('mobile_legends', language),
        callback_data="game_mobile_legends"
    )
    builder.button(
        text=translator.get('back', language),
        callback_data="back_to_main"
    )
    
    builder.adjust(1)
    return builder.as_markup()


def get_amounts_keyboard(game: str, language: str = 'uz') -> InlineKeyboardMarkup:
    """Miqdorlarni tanlash klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    amounts = db.get_game_amounts(game)
    
    for amount in amounts:
        price = db.get_price(game, amount)
        builder.button(
            text=f"{amount} - {price:,} so'm".replace(',', ' '),
            callback_data=f"amount_{game}_{amount}"
        )
    
    builder.button(
        text=translator.get('back', language),
        callback_data="back_to_games"
    )
    
    builder.adjust(1)
    return builder.as_markup()


def get_cancel_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Bekor qilish klaviaturasi"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text=translator.get('cancel', language))
    
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def get_admin_menu(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Admin menyu klaviaturasi"""
    builder = ReplyKeyboardBuilder()
    
    pending_count = len(db.get_pending_orders())
    
    builder.button(
        text=translator.get('pending_orders', language, count=pending_count)
    )
    builder.button(text=translator.get('all_orders', language))
    builder.button(text=translator.get('users_list', language))
    builder.button(text=translator.get('manage_prices', language))
    builder.button(text=translator.get('broadcast', language))
    builder.button(text=translator.get('statistics', language))
    builder.button(text=translator.get('main_menu_btn', language))
    
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def get_order_actions_keyboard(order_id: int, language: str = 'uz') -> InlineKeyboardMarkup:
    """Buyurtma ustida amallar klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text=translator.get('approve_order', language),
        callback_data=f"approve_{order_id}"
    )
    builder.button(
        text=translator.get('reject_order', language),
        callback_data=f"reject_{order_id}"
    )
    
    builder.adjust(2)
    return builder.as_markup()


def get_orders_list_keyboard(orders: list, language: str = 'uz') -> InlineKeyboardMarkup:
    """Buyurtmalar ro'yxati klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    for order in orders[:10]:  # Faqat oxirgi 10 ta
        status_emoji = '⏳' if order['status'] == 'pending' else '✅' if order['status'] == 'approved' else '❌'
        builder.button(
            text=f"{status_emoji} #{order['id']} - {order['game']}",
            callback_data=f"view_order_{order['id']}"
        )
    
    builder.adjust(1)
    return builder.as_markup()


def get_price_management_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Narxlarni boshqarish klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    prices = db.get_all_prices()
    
    for game in prices.keys():
        builder.button(
            text=f"💰 {game}",
            callback_data=f"manage_price_{game}"
        )
    
    builder.button(
        text=translator.get('back', language),
        callback_data="back_to_admin"
    )
    
    builder.adjust(1)
    return builder.as_markup()


def get_game_prices_keyboard(game: str, language: str = 'uz') -> InlineKeyboardMarkup:
    """O'yin narxlari klaviaturasi"""
    builder = InlineKeyboardBuilder()
    
    amounts = db.get_game_amounts(game)
    
    for amount in amounts:
        price = db.get_price(game, amount)
        builder.button(
            text=f"{amount} - {price:,} so'm".replace(',', ' '),
            callback_data=f"edit_price_{game}_{amount}"
        )
    
    builder.button(
        text=translator.get('back', language),
        callback_data="back_to_price_mgmt"
    )
    
    builder.adjust(1)
    return builder.as_markup()

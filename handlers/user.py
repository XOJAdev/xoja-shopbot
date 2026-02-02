from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
import os

from database.db import Database
from keyboards.keyboards import (
    get_language_keyboard, get_main_menu, get_games_keyboard,
    get_amounts_keyboard, get_cancel_keyboard
)
from utils.helpers import translator, validate_game_id, GAMES, format_number

router = Router()
db = Database()


class OrderStates(StatesGroup):
    """Buyurtma holatlari"""
    waiting_for_game_id = State()
    waiting_for_receipt = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start komandasi"""
    user = db.get_user(message.from_user.id)
    
    if not user:
        # Yangi foydalanuvchi
        db.add_user(
            user_id=message.from_user.id,
            username=message.from_user.username or "",
            first_name=message.from_user.first_name or "",
            language='uz'
        )
        
        await message.answer(
            translator.get('welcome', 'uz'),
            reply_markup=get_language_keyboard()
        )
    else:
        # Mavjud foydalanuvchi
        language = user['language']
        await message.answer(
            translator.get('main_menu', language),
            reply_markup=get_main_menu(language)
        )


@router.callback_query(F.data.startswith('lang_'))
async def process_language_selection(callback: CallbackQuery):
    """Til tanlash"""
    language = callback.data.split('_')[1]
    
    db.update_user_language(callback.from_user.id, language)
    
    await callback.message.edit_text(
        translator.get('language_changed', language)
    )
    
    await callback.message.answer(
        translator.get('main_menu', language),
        reply_markup=get_main_menu(language)
    )
    
    await callback.answer()


@router.message(F.text.in_([
    translator.get('select_language', 'uz'),
    translator.get('select_language', 'ru'),
    translator.get('select_language', 'en')
]))
async def select_language(message: Message):
    """Til tanlash menyusi"""
    user = db.get_user(message.from_user.id)
    language = user['language'] if user else 'uz'
    
    await message.answer(
        translator.get('welcome', language),
        reply_markup=get_language_keyboard()
    )


@router.message(F.text.in_([
    translator.get('make_donation', 'uz'),
    translator.get('make_donation', 'ru'),
    translator.get('make_donation', 'en')
]))
async def make_donation(message: Message):
    """Donat qilish"""
    user = db.get_user(message.from_user.id)
    language = user['language'] if user else 'uz'
    
    await message.answer(
        translator.get('select_game', language),
        reply_markup=get_games_keyboard(language)
    )


@router.callback_query(F.data.startswith('game_'))
async def process_game_selection(callback: CallbackQuery, state: FSMContext):
    """O'yin tanlash"""

    user_id = callback.from_user.id
    user = db.get_user(user_id)

    # Agar user bazada bo‘lmasa — uni yaratamiz
    if user is None:
        db.add_user(user_id, "uz")  # default til uz
        user = db.get_user(user_id)

    language = user["language"]

    game_key = callback.data.replace('game_', '')
    game_name = GAMES.get(game_key, 'PUBG Mobile')

    await state.update_data(game=game_name)

    await callback.message.edit_text(
        translator.get('select_amount', language),
        reply_markup=get_amounts_keyboard(game_name, language)
    )

    await callback.answer()



@router.callback_query(F.data.startswith('amount_'))
async def process_amount_selection(callback: CallbackQuery, state: FSMContext):
    """Miqdor tanlash"""
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    parts = callback.data.split('_', 2)
    game = parts[1]
    amount = parts[2]
    
    await state.update_data(amount=amount)
    
    await callback.message.edit_text(
        translator.get('enter_game_id', language)
    )
    
    await callback.message.answer(
        "⬇️",
        reply_markup=get_cancel_keyboard(language)
    )
    
    await state.set_state(OrderStates.waiting_for_game_id)
    await callback.answer()


@router.message(OrderStates.waiting_for_game_id)
async def process_game_id(message: Message, state: FSMContext):
    """Game ID qabul qilish"""
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    # Bekor qilish
    if message.text in [
        translator.get('cancel', 'uz'),
        translator.get('cancel', 'ru'),
        translator.get('cancel', 'en')
    ]:
        await state.clear()
        await message.answer(
            translator.get('main_menu', language),
            reply_markup=get_main_menu(language)
        )
        return
    
    game_id = message.text.strip()
    
    if not validate_game_id(game_id):
        await message.answer(
            translator.get('invalid_game_id', language)
        )
        return
    
    await state.update_data(game_id=game_id)
    
    # To'lov ma'lumotlarini ko'rsatish
    data = await state.get_data()
    game = data['game']
    amount = data['amount']
    price = db.get_price(game, amount)
    card_number = db.get_setting('card_number')
    
    payment_text = translator.get(
        'payment_info',
        language,
        game=game,
        amount=amount,
        price=format_number(price),
        game_id=game_id,
        card_number=card_number
    )
    
    await message.answer(payment_text, reply_markup=get_cancel_keyboard(language))
    await message.answer(translator.get('send_receipt', language))
    
    await state.set_state(OrderStates.waiting_for_receipt)


@router.message(OrderStates.waiting_for_receipt, F.photo)
async def process_receipt(message: Message, state: FSMContext):
    """Chek rasmini qabul qilish"""
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    # Rasmni saqlash
    photo = message.photo[-1]
    file_name = f"receipt_{message.from_user.id}_{datetime.now().timestamp()}.jpg"
    file_path = os.path.join("checks", file_name)
    
    await message.bot.download(photo, destination=file_path)
    
    # Buyurtma yaratish
    data = await state.get_data()
    game = data['game']
    amount = data['amount']
    game_id = data['game_id']
    price = db.get_price(game, amount)
    
    order_id = db.create_order(
        user_id=message.from_user.id,
        game=game,
        amount=amount,
        game_id=game_id,
        price=price,
        receipt_path=file_path
    )
    
    await message.answer(
        translator.get('order_received', language, order_id=order_id),
        reply_markup=get_main_menu(language)
    )
    
    await state.clear()
    
    # Adminlarga xabar yuborish
    await notify_admins_new_order(message.bot, order_id, user)


@router.message(OrderStates.waiting_for_receipt)
async def invalid_receipt(message: Message):
    """Noto'g'ri chek"""
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    # Bekor qilish
    if message.text in [
        translator.get('cancel', 'uz'),
        translator.get('cancel', 'ru'),
        translator.get('cancel', 'en')
    ]:
        await message.reply(
            translator.get('main_menu', language),
            reply_markup=get_main_menu(language)
        )
        return
    
    await message.answer(translator.get('receipt_required', language))


@router.message(F.text.in_([
    translator.get('my_orders', 'uz'),
    translator.get('my_orders', 'ru'),
    translator.get('my_orders', 'en')
]))
async def my_orders(message: Message):
    """Mening buyurtmalarim"""
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    orders = db.get_user_orders(message.from_user.id)
    
    if not orders:
        await message.answer(
            translator.get('no_orders', language),
            reply_markup=get_main_menu(language)
        )
        return
    
    text = translator.get('my_orders_list', language)
    
    for order in orders[:10]:  # Oxirgi 10 ta
        status = translator.get(f'order_status_{order["status"]}', language)
        text += f"\n🔢 #{order['id']}\n"
        text += f"🎮 {order['game']}\n"
        text += f"💰 {order['amount']}\n"
        text += f"📊 {status}\n"
        text += f"📅 {order['created_at'][:16]}\n"
        text += "─" * 30 + "\n"
    
    await message.answer(text, reply_markup=get_main_menu(language))


@router.message(F.text.in_([
    translator.get('help', 'uz'),
    translator.get('help', 'ru'),
    translator.get('help', 'en')
]))
async def help_command(message: Message):
    """Yordam"""
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    support_username = db.get_setting('support_username')
    
    await message.answer(
        translator.get('help_text', language, support_username=support_username),
        reply_markup=get_main_menu(language)
    )


@router.callback_query(F.data == 'back_to_main')
async def back_to_main(callback: CallbackQuery):
    """Asosiy menyuga qaytish"""
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    await callback.message.delete()
    await callback.message.answer(
        translator.get('main_menu', language),
        reply_markup=get_main_menu(language)
    )
    await callback.answer()


@router.callback_query(F.data == 'back_to_games')
async def back_to_games(callback: CallbackQuery):
    """O'yinlar menyusiga qaytish"""
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    await callback.message.edit_text(
        translator.get('select_game', language),
        reply_markup=get_games_keyboard(language)
    )
    await callback.answer()


async def notify_admins_new_order(bot, order_id: int, user: dict):
    """Adminlarga yangi buyurtma haqida xabar yuborish"""
    order = db.get_order(order_id)
    if not order:
        return
    
    admins = [u for u in db.get_all_users() if u['is_admin'] == 1]
    
    for admin in admins:
        language = admin['language']
        
        text = translator.get(
            'new_order_admin',
            language,
            order_id=order_id,
            username=user.get('username', 'N/A'),
            user_id=user['user_id'],
            game=order['game'],
            amount=order['amount'],
            price=format_number(order['price']),
            game_id=order['game_id'],
            time=order['created_at'][:16]
        )
        
        try:
            # Chek rasmini yuborish
            from aiogram.types import FSInputFile
            from keyboards.keyboards import get_order_actions_keyboard
            
            photo = FSInputFile(order['receipt_path'])
            await bot.send_photo(
                admin['user_id'],
                photo=photo,
                caption=text,
                reply_markup=get_order_actions_keyboard(order_id, language)
            )
        except Exception as e:
            print(f"Admin {admin['user_id']}ga xabar yuborishda xatolik: {e}")

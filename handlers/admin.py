from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from database.db import Database
from keyboards.keyboards import (
    get_admin_menu, get_order_actions_keyboard,
    get_price_management_keyboard, get_game_prices_keyboard,
    get_main_menu
)
from utils.helpers import translator, format_number

router = Router()
db = Database()


class AdminStates(StatesGroup):
    """Admin holatlari"""
    waiting_for_rejection_reason = State()
    waiting_for_broadcast_message = State()
    waiting_for_new_price = State()


def check_admin(user_id: int) -> bool:
    """Admin ekanligini tekshirish"""
    return db.is_admin(user_id)


@router.message(Command('admin'))
async def admin_panel(message: Message):
    """Admin panel"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    stats = db.get_statistics()
    
    text = translator.get(
        'admin_panel',
        language,
        total_orders=stats['total_orders'],
        today_orders=stats['today_orders'],
        month_orders=stats['month_orders'],
        total_revenue=format_number(stats['total_revenue'])
    )
    
    await message.answer(
        text,
        reply_markup=get_admin_menu(language)
    )


@router.message(F.text.contains("Yangi buyurtmalar") | 
                F.text.contains("Новые заказы") | 
                F.text.contains("New Orders"))
async def pending_orders(message: Message):
    """Yangi buyurtmalar"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    orders = db.get_pending_orders()
    
    if not orders:
        await message.answer(
            "📭 " + translator.get('no_orders', language),
            reply_markup=get_admin_menu(language)
        )
        return
    
    for order in orders:
        order_user = db.get_user(order['user_id'])
        
        text = translator.get(
            'new_order_admin',
            language,
            order_id=order['id'],
            username=order_user.get('username', 'N/A'),
            user_id=order['user_id'],
            game=order['game'],
            amount=order['amount'],
            price=format_number(order['price']),
            game_id=order['game_id'],
            time=order['created_at'][:16]
        )
        
        try:
            photo = FSInputFile(order['receipt_path'])
            await message.answer_photo(
                photo=photo,
                caption=text,
                reply_markup=get_order_actions_keyboard(order['id'], language)
            )
        except Exception as e:
            await message.answer(
                text + f"\n\n❌ Chek rasmini yuklashda xatolik",
                reply_markup=get_order_actions_keyboard(order['id'], language)
            )


@router.message(F.text.contains("Barcha buyurtmalar") | 
                F.text.contains("Все заказы") | 
                F.text.contains("All Orders"))
async def all_orders(message: Message):
    """Barcha buyurtmalar"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    orders = db.get_all_orders()
    
    if not orders:
        await message.answer(
            translator.get('no_orders', language),
            reply_markup=get_admin_menu(language)
        )
        return
    
    text = "📋 " + translator.get('all_orders', language) + "\n\n"
    
    for order in orders[:20]:  # Oxirgi 20 ta
        status = translator.get(f'order_status_{order["status"]}', language)
        text += f"🔢 #{order['id']} - {status}\n"
        text += f"👤 User: {order['user_id']}\n"
        text += f"🎮 {order['game']} - {order['amount']}\n"
        text += f"💰 {format_number(order['price'])} so'm\n"
        text += f"📅 {order['created_at'][:16]}\n"
        text += "─" * 30 + "\n"
    
    await message.answer(text, reply_markup=get_admin_menu(language))


@router.callback_query(F.data.startswith('approve_'))
async def approve_order(callback: CallbackQuery):
    """Buyurtmani tasdiqlash"""
    if not check_admin(callback.from_user.id):
        await callback.answer("⛔ Admin emas!")
        return
    
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    order_id = int(callback.data.split('_')[1])
    order = db.get_order(order_id)
    
    if not order:
        await callback.answer(translator.get('order_not_found', language))
        return
    
    # Buyurtmani tasdiqlash
    db.approve_order(order_id)
    
    await callback.message.edit_caption(
        caption=callback.message.caption + "\n\n✅ " + 
        translator.get('order_approved_admin', language, order_id=order_id)
    )
    
    # Foydalanuvchiga xabar yuborish
    order_user = db.get_user(order['user_id'])
    user_language = order_user['language']
    
    await callback.bot.send_message(
        order['user_id'],
        translator.get(
            'order_approved',
            user_language,
            order_id=order_id,
            game=order['game'],
            amount=order['amount']
        )
    )
    
    await callback.answer("✅ Tasdiqlandi!")


@router.callback_query(F.data.startswith('reject_'))
async def start_reject_order(callback: CallbackQuery, state: FSMContext):
    """Buyurtmani rad etishni boshlash"""
    if not check_admin(callback.from_user.id):
        await callback.answer("⛔ Admin emas!")
        return
    
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    order_id = int(callback.data.split('_')[1])
    
    await state.update_data(reject_order_id=order_id)
    await state.set_state(AdminStates.waiting_for_rejection_reason)
    
    await callback.message.answer(
        translator.get('order_rejected_admin', language, order_id=order_id)
    )
    
    await callback.answer()


@router.message(AdminStates.waiting_for_rejection_reason)
async def process_rejection_reason(message: Message, state: FSMContext):
    """Rad etish sababini qabul qilish"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    data = await state.get_data()
    order_id = data['reject_order_id']
    reason = message.text
    
    order = db.get_order(order_id)
    
    if not order:
        await message.answer(translator.get('order_not_found', language))
        await state.clear()
        return
    
    # Buyurtmani rad etish
    db.reject_order(order_id, reason)
    
    await message.answer(
        translator.get('rejection_reason_received', language),
        reply_markup=get_admin_menu(language)
    )
    
    # Foydalanuvchiga xabar yuborish
    order_user = db.get_user(order['user_id'])
    user_language = order_user['language']
    
    await message.bot.send_message(
        order['user_id'],
        translator.get(
            'order_rejected',
            user_language,
            order_id=order_id,
            reason=reason
        )
    )
    
    await state.clear()


@router.message(F.text.contains("Foydalanuvchilar") | 
                F.text.contains("Пользователи") | 
                F.text.contains("Users"))
async def users_list(message: Message):
    """Foydalanuvchilar ro'yxati"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    users = db.get_all_users()
    
    text = translator.get('total_users', language, count=len(users))
    
    for u in users[:20]:  # Birinchi 20 ta
        orders_count = len(db.get_user_orders(u['user_id']))
        text += translator.get(
            'user_info',
            language,
            username=u['username'] or u['first_name'],
            user_id=u['user_id'],
            joined=u['joined_date'][:10],
            orders=orders_count
        )
    
    await message.answer(text, reply_markup=get_admin_menu(language))


@router.message(F.text.contains("Narxlarni boshqarish") | 
                F.text.contains("Управление ценами") | 
                F.text.contains("Manage Prices"))
async def manage_prices_menu(message: Message):
    """Narxlarni boshqarish menyusi"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    await message.answer(
        translator.get('manage_prices', language),
        reply_markup=get_price_management_keyboard(language)
    )


@router.callback_query(F.data.startswith('manage_price_'))
async def show_game_prices(callback: CallbackQuery):
    """O'yin narxlarini ko'rsatish"""
    if not check_admin(callback.from_user.id):
        await callback.answer("⛔ Admin emas!")
        return
    
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    game = callback.data.replace('manage_price_', '')
    
    await callback.message.edit_text(
        f"💰 {game}",
        reply_markup=get_game_prices_keyboard(game, language)
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith('edit_price_'))
async def start_edit_price(callback: CallbackQuery, state: FSMContext):
    """Narxni tahrirlashni boshlash"""
    if not check_admin(callback.from_user.id):
        await callback.answer("⛔ Admin emas!")
        return
    
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    parts = callback.data.split('_', 3)
    game = parts[2]
    amount = parts[3]
    
    await state.update_data(edit_game=game, edit_amount=amount)
    await state.set_state(AdminStates.waiting_for_new_price)
    
    await callback.message.answer(
        translator.get('enter_new_price', language, game=game, amount=amount)
    )
    
    await callback.answer()


@router.message(AdminStates.waiting_for_new_price)
async def process_new_price(message: Message, state: FSMContext):
    """Yangi narxni qabul qilish"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    if not message.text.isdigit():
        await message.answer(translator.get('invalid_price', language))
        return
    
    new_price = int(message.text)
    data = await state.get_data()
    game = data['edit_game']
    amount = data['edit_amount']
    
    db.update_price(game, amount, new_price)
    
    await message.answer(
        translator.get('price_updated', language, 
                      game=game, amount=amount, price=format_number(new_price)),
        reply_markup=get_admin_menu(language)
    )
    
    await state.clear()


@router.message(F.text.contains("Xabar yuborish") | 
                F.text.contains("Рассылка") | 
                F.text.contains("Broadcast"))
async def start_broadcast(message: Message, state: FSMContext):
    """Reklama yuborishni boshlash"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    await message.answer(translator.get('broadcast_prompt', language))
    await state.set_state(AdminStates.waiting_for_broadcast_message)


@router.message(AdminStates.waiting_for_broadcast_message)
async def process_broadcast(message: Message, state: FSMContext):
    """Reklama xabarini yuborish"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    users = db.get_all_users()
    sent_count = 0
    
    for u in users:
        try:
            await message.bot.send_message(u['user_id'], message.text)
            sent_count += 1
        except Exception as e:
            print(f"User {u['user_id']}ga xabar yuborishda xatolik: {e}")
    
    await message.answer(
        translator.get('broadcast_sent', language, count=sent_count),
        reply_markup=get_admin_menu(language)
    )
    
    await state.clear()


@router.message(F.text.contains("Statistika") | 
                F.text.contains("Статистика") | 
                F.text.contains("Statistics"))
async def show_statistics(message: Message):
    """Statistikani ko'rsatish"""
    if not check_admin(message.from_user.id):
        return
    
    user = db.get_user(message.from_user.id)
    language = user['language']
    
    stats = db.get_statistics()
    
    text = translator.get(
        'statistics_text',
        language,
        today_orders=stats['today_orders'],
        month_orders=stats['month_orders'],
        total_orders=stats['total_orders'],
        today_revenue=format_number(stats['today_revenue']),
        month_revenue=format_number(stats['month_revenue']),
        total_revenue=format_number(stats['total_revenue']),
        total_users=stats['total_users']
    )
    
    await message.answer(text, reply_markup=get_admin_menu(language))


@router.callback_query(F.data == 'back_to_admin')
async def back_to_admin(callback: CallbackQuery):
    """Admin menyusiga qaytish"""
    if not check_admin(callback.from_user.id):
        await callback.answer("⛔ Admin emas!")
        return
    
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    await callback.message.delete()
    await callback.message.answer(
        translator.get('admin_menu', language),
        reply_markup=get_admin_menu(language)
    )
    await callback.answer()


@router.callback_query(F.data == 'back_to_price_mgmt')
async def back_to_price_mgmt(callback: CallbackQuery):
    """Narxlar menyusiga qaytish"""
    if not check_admin(callback.from_user.id):
        await callback.answer("⛔ Admin emas!")
        return
    
    user = db.get_user(callback.from_user.id)
    language = user['language']
    
    await callback.message.edit_text(
        translator.get('manage_prices', language),
        reply_markup=get_price_management_keyboard(language)
    )
    await callback.answer()


@router.message(F.text.in_([
    translator.get('main_menu_btn', 'uz'),
    translator.get('main_menu_btn', 'ru'),
    translator.get('main_menu_btn', 'en')
]))
async def back_to_main_menu(message: Message, state: FSMContext):
    """Asosiy menyuga qaytish"""
    await state.clear()
    
    user = db.get_user(message.from_user.id)
    language = user['language'] if user else 'uz'
    
    await message.answer(
        translator.get('main_menu', language),
        reply_markup=get_main_menu(language)
    )

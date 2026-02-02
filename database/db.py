import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
import json


class Database:
    def __init__(self, db_path: str = "donat_bot.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Ma'lumotlar bazasini yaratish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Foydalanuvchilar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'uz',
                joined_date TEXT,
                is_admin INTEGER DEFAULT 0
            )
        ''')
        
        # Buyurtmalar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game TEXT,
                amount TEXT,
                game_id TEXT,
                price INTEGER,
                receipt_path TEXT,
                status TEXT DEFAULT 'pending',
                rejection_reason TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Narxlar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game TEXT,
                amount TEXT,
                price INTEGER
            )
        ''')
        
        # Sozlamalar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Standart narxlarni qo'shish
        self.init_default_prices()
        self.init_default_settings()
    
    def init_default_prices(self):
        """Standart narxlarni qo'shish"""
        default_prices = [
            ('PUBG Mobile', '60 UC', 10000),
            ('PUBG Mobile', '325 UC', 50000),
            ('PUBG Mobile', '660 UC', 100000),
            ('PUBG Mobile', '1800 UC', 250000),
            ('Telegram Premium', '1 oy', 25000),
            ('Telegram Premium', '3 oy', 70000),
            ('Telegram Premium', '6 oy', 130000),
            ('Telegram Premium', '12 oy', 240000),
            ('Telegram Stars', '100 Stars', 15000),
            ('Telegram Stars', '500 Stars', 70000),
            ('Telegram Stars', '1000 Stars', 130000),
            ('Telegram Stars', '2500 Stars', 300000),
            ('Mobile Legends', '100 Almaz', 12000),
            ('Mobile Legends', '500 Almaz', 55000),
            ('Mobile Legends', '1000 Almaz', 105000),
            ('Mobile Legends', '2500 Almaz', 250000),
        ]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for game, amount, price in default_prices:
            cursor.execute('''
                INSERT OR IGNORE INTO prices (game, amount, price)
                SELECT ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM prices WHERE game = ? AND amount = ?
                )
            ''', (game, amount, price, game, amount))
        
        conn.commit()
        conn.close()
    
    def init_default_settings(self):
        """Standart sozlamalarni qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('card_number', '8600 1234 5678 9012')
        ''')
        
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value)
            VALUES ('support_username', 'support')
        ''')
        
        conn.commit()
        conn.close()
    
    # ======= FOYDALANUVCHILAR =======
    
    def add_user(self, user_id: int, username: str, first_name: str, language: str = 'uz'):
        """Yangi foydalanuvchi qo'shish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, first_name, language, joined_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, language, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Foydalanuvchi ma'lumotlarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def update_user_language(self, user_id: int, language: str):
        """Foydalanuvchi tilini yangilash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET language = ? WHERE user_id = ?
        ''', (language, user_id))
        
        conn.commit()
        conn.close()
    
    def get_all_users(self) -> List[Dict]:
        """Barcha foydalanuvchilarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users ORDER BY joined_date DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def is_admin(self, user_id: int) -> bool:
        """Foydalanuvchi admin ekanligini tekshirish"""
        user = self.get_user(user_id)
        if user:
            return user['is_admin'] == 1
        return False
    
    def set_admin(self, user_id: int, is_admin: bool = True):
        """Foydalanuvchini admin qilish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET is_admin = ? WHERE user_id = ?
        ''', (1 if is_admin else 0, user_id))
        
        conn.commit()
        conn.close()
    
    # ======= BUYURTMALAR =======
    
    def create_order(self, user_id: int, game: str, amount: str, game_id: str, 
                    price: int, receipt_path: str) -> int:
        """Yangi buyurtma yaratish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO orders (user_id, game, amount, game_id, price, receipt_path, 
                              status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?)
        ''', (user_id, game, amount, game_id, price, receipt_path, now, now))
        
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return order_id
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """Buyurtma ma'lumotlarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Foydalanuvchi buyurtmalarini olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_pending_orders(self) -> List[Dict]:
        """Kutilayotgan buyurtmalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at ASC
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_all_orders(self) -> List[Dict]:
        """Barcha buyurtmalarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def approve_order(self, order_id: int):
        """Buyurtmani tasdiqlash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders SET status = 'approved', updated_at = ? WHERE id = ?
        ''', (datetime.now().isoformat(), order_id))
        
        conn.commit()
        conn.close()
    
    def reject_order(self, order_id: int, reason: str):
        """Buyurtmani rad etish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders SET status = 'rejected', rejection_reason = ?, 
                            updated_at = ? WHERE id = ?
        ''', (reason, datetime.now().isoformat(), order_id))
        
        conn.commit()
        conn.close()
    
    # ======= NARXLAR =======
    
    def get_price(self, game: str, amount: str) -> Optional[int]:
        """Narxni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price FROM prices WHERE game = ? AND amount = ?
        ''', (game, amount))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row['price']
        return None
    
    def get_game_amounts(self, game: str) -> List[str]:
        """O'yin uchun mavjud miqdorlarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT amount FROM prices WHERE game = ? ORDER BY price ASC
        ''', (game,))
        rows = cursor.fetchall()
        conn.close()
        
        return [row['amount'] for row in rows]
    
    def update_price(self, game: str, amount: str, price: int):
        """Narxni yangilash"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE prices SET price = ? WHERE game = ? AND amount = ?
        ''', (price, game, amount))
        
        conn.commit()
        conn.close()
    
    def get_all_prices(self) -> Dict[str, List[Dict]]:
        """Barcha narxlarni olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM prices ORDER BY game, price ASC')
        rows = cursor.fetchall()
        conn.close()
        
        prices_dict = {}
        for row in rows:
            game = row['game']
            if game not in prices_dict:
                prices_dict[game] = []
            prices_dict[game].append({
                'amount': row['amount'],
                'price': row['price']
            })
        
        return prices_dict
    
    # ======= SOZLAMALAR =======
    
    def get_setting(self, key: str) -> Optional[str]:
        """Sozlamani olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row['value']
        return None
    
    def set_setting(self, key: str, value: str):
        """Sozlamani o'rnatish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
        
        conn.commit()
        conn.close()
    
    # ======= STATISTIKA =======
    
    def get_statistics(self) -> Dict:
        """Statistikani olish"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Jami buyurtmalar
        cursor.execute('SELECT COUNT(*) as count FROM orders')
        total_orders = cursor.fetchone()['count']
        
        # Bugungi buyurtmalar
        today = datetime.now().date().isoformat()
        cursor.execute('''
            SELECT COUNT(*) as count FROM orders 
            WHERE date(created_at) = ?
        ''', (today,))
        today_orders = cursor.fetchone()['count']
        
        # Oylik buyurtmalar
        month = datetime.now().strftime('%Y-%m')
        cursor.execute('''
            SELECT COUNT(*) as count FROM orders 
            WHERE strftime('%Y-%m', created_at) = ?
        ''', (month,))
        month_orders = cursor.fetchone()['count']
        
        # Jami tushum
        cursor.execute('''
            SELECT SUM(price) as total FROM orders WHERE status = 'approved'
        ''')
        total_revenue = cursor.fetchone()['total'] or 0
        
        # Bugungi tushum
        cursor.execute('''
            SELECT SUM(price) as total FROM orders 
            WHERE status = 'approved' AND date(created_at) = ?
        ''', (today,))
        today_revenue = cursor.fetchone()['total'] or 0
        
        # Oylik tushum
        cursor.execute('''
            SELECT SUM(price) as total FROM orders 
            WHERE status = 'approved' AND strftime('%Y-%m', created_at) = ?
        ''', (month,))
        month_revenue = cursor.fetchone()['total'] or 0
        
        # Jami foydalanuvchilar
        cursor.execute('SELECT COUNT(*) as count FROM users')
        total_users = cursor.fetchone()['count']
        
        conn.close()
        
        return {
            'total_orders': total_orders,
            'today_orders': today_orders,
            'month_orders': month_orders,
            'total_revenue': total_revenue,
            'today_revenue': today_revenue,
            'month_revenue': month_revenue,
            'total_users': total_users
        }

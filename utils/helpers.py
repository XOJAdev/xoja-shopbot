import json
import os
from typing import Dict


class Translator:
    """Ko'p tillilik uchun translator"""
    
    def __init__(self):
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Barcha tillarni yuklash"""
        languages_dir = "languages"
        for lang_file in ['uz.json', 'ru.json', 'en.json']:
            lang_code = lang_file.split('.')[0]
            filepath = os.path.join(languages_dir, lang_file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                self.translations[lang_code] = json.load(f)
    
    def get(self, key: str, language: str = 'uz', **kwargs) -> str:
        """Tarjimani olish"""
        if language not in self.translations:
            language = 'uz'
        
        text = self.translations[language].get(key, key)
        
        # Parametrlarni almashtirish
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        
        return text


# Global translator obyekti
translator = Translator()


def format_number(number: int) -> str:
    """Sonni formatlash (10000 -> 10 000)"""
    return "{:,}".format(number).replace(',', ' ')


def get_game_emoji(game: str) -> str:
    """O'yin uchun emoji olish"""
    emoji_map = {
        'PUBG Mobile': '🎮',
        'Telegram Premium': '⭐',
        'Telegram Stars': '⭐',
        'Mobile Legends': '💎'
    }
    return emoji_map.get(game, '🎮')


def get_status_emoji(status: str) -> str:
    """Status uchun emoji olish"""
    emoji_map = {
        'pending': '⏳',
        'approved': '✅',
        'rejected': '❌'
    }
    return emoji_map.get(status, '❓')


# Game va amount mapping
GAMES = {
    'pubg': 'PUBG Mobile',
    'telegram_premium': 'Telegram Premium',
    'telegram_stars': 'Telegram Stars',
    'mobile_legends': 'Mobile Legends'
}


def get_game_key(game_name: str) -> str:
    """O'yin nomidan kalit olish"""
    for key, value in GAMES.items():
        if value == game_name:
            return key
    return 'pubg'


def validate_game_id(game_id: str) -> bool:
    """Game ID tekshirish"""
    # Faqat raqamlar va minimal uzunlik
    return game_id.isdigit() and len(game_id) >= 5

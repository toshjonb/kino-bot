from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():

    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton("🔥 Mashhur kinolar", callback_data="top"))

    kb.add(InlineKeyboardButton("🎬 Yangi kinolar", callback_data="new"))

    kb.add(InlineKeyboardButton("🔎 Kino qidirish", callback_data="search"))

    return kb

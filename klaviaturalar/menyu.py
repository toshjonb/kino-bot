from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    resize_keyboard=True
)

menu.add(
    KeyboardButton("🔎 Kino qidirish")
)

menu.add(
    KeyboardButton("🎬 Kategoriyalar"),
    KeyboardButton("⭐ Mashhur")
)

menu.add(
    KeyboardButton("🆕 Yangi kinolar")
)

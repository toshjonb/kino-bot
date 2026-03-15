from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import TOKEN
from database import create_db
from search import search_movie
from keyboards.menu import menu

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await message.answer(
        "🎬 Kino botga xush kelibsiz\n\n"
        "Kino nomi yoki kodini yozing",
        reply_markup=menu
    )


@dp.message_handler()
async def search(message: types.Message):

    movies = await search_movie(message.text)

    if not movies:
        await message.answer("❌ Kino topilmadi")
        return

    for movie in movies:

        await message.answer_video(
            movie["file_id"],
            caption=f"""
🎬 {movie["name"]}

📂 {movie["category"]}
⭐ {movie["views"]} ko‘rildi
"""
        )


async def on_startup(dp):
    await create_db()


executor.start_polling(dp, on_startup=on_startup)

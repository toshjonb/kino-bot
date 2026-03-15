from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import TOKEN, CHANNEL, ADMIN
from database import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await message.answer("🎬 Kino bot")


# ADMIN PANEL
@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):

    if message.from_user.id != ADMIN:
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("➕ Kino qo‘shish")

    await message.answer("👑 Admin panel", reply_markup=kb)


# kino ID
@dp.message_handler(lambda message: message.text.isdigit())
async def movie_code(message: types.Message):

    movie = await get_movie_by_id(message.text)

    if not movie:

        await message.answer("❌ Kino topilmadi")
        return

    await bot.send_video(
        message.chat.id,
        movie[3],
        caption=movie[4]
    )


# SEARCH (ENG OXIRIDA BO‘LISHI SHART)
@dp.message_handler()
async def search(message: types.Message):

    movies = await search_movie(message.text)

    if not movies:

        await message.answer("❌ Kino topilmadi")
        return

    for m in movies:

        await message.answer_video(
            m[3],
            caption=f"{m[1]}\nID: {m[0]}"
        )


executor.start_polling(dp)

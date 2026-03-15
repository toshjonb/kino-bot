from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import TOKEN, CHANNEL, ADMIN
from database import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def check_sub(user_id):

    member = await bot.get_chat_member(CHANNEL, user_id)

    if member.status in ["member","administrator","creator"]:
        return True

    return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    if not await check_sub(message.from_user.id):

        await message.answer(
            f"❗ Kanalga obuna bo‘ling\n\n{CHANNEL}"
        )
        return

    await message.answer(
        "🎬 Kino bot\n\nKino nomi yoki kodini yozing"
    )


# kino ID bilan
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

    await add_view(movie[0])


# kino nomi bilan qidiruv
@dp.message_handler()
async def search(message: types.Message):

    movies = await search_movie(message.text)

    if not movies:

        await message.answer("❌ Kino topilmadi")
        return

    for m in movies:

        await message.answer_video(
            m[3],
            caption=f"""
🎬 {m[1]}

📂 {m[2]}
⭐ {m[5]} ko‘rildi
ID: {m[0]}
"""
        )


# admin panel
@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):

    if message.from_user.id != ADMIN:
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("➕ Kino qo‘shish")

    await message.answer(
        "👑 Admin panel",
        reply_markup=kb
    )


# kino qo‘shish
@dp.message_handler(lambda message: message.text == "➕ Kino qo‘shish")
async def add_movie_start(message: types.Message):

    if message.from_user.id != ADMIN:
        return

    await message.answer("🎬 Kino nomini yuboring")


async def on_startup(dp):

    await create_db()


executor.start_polling(dp, on_startup=on_startup)

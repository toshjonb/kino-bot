from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import TOKEN, CHANNEL, ADMIN
from database import create_db, get_movie_by_id, add_view, top_movies

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
            f"❗ Botdan foydalanish uchun kanalga obuna bo‘ling\n\n{CHANNEL}"
        )
        return

    await message.answer(
        "🎬 Kino botga xush kelibsiz\n\nKino kodini yozing"
    )


@dp.message_handler(lambda message: message.text.isdigit())
async def movie_code(message: types.Message):

    movie = await get_movie_by_id(message.text)

    if not movie:

        await message.answer("❌ Kino topilmadi")
        return

    await bot.send_video(
        message.chat.id,
        movie[3],
        caption=f"""
🎬 {movie[1]}

📂 {movie[2]}
⭐ {movie[4]} ko‘rildi
"""
    )

    await add_view(movie[0])


@dp.message_handler(commands=['top'])
async def top(message: types.Message):

    movies = await top_movies()

    text = "⭐ Eng mashhur kinolar\n\n"

    for m in movies:

        text += f"{m[0]}. {m[1]} ({m[4]} views)\n"

    await message.answer(text)


@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):

    if message.from_user.id != ADMIN:
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add("➕ Kino qo‘shish")
    kb.add("📊 Statistika")

    await message.answer(
        "👑 Admin panel",
        reply_markup=kb
    )


async def on_startup(dp):
    await create_db()


executor.start_polling(dp, on_startup=on_startup)

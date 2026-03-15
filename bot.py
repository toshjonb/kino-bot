from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN, CHANNEL, ADMIN
from database import *

bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# STATE
class AddMovie(StatesGroup):
    name = State()
    category = State()
    video = State()


# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🎬 Kino botga xush kelibsiz")


# ADMIN PANEL
@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):

    if message.from_user.id != ADMIN:
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("➕ Kino qo‘shish")

    await message.answer("👑 Admin panel", reply_markup=kb)


# KINO QO‘SHISH BOSHLASH
@dp.message_handler(lambda message: message.text == "➕ Kino qo‘shish")
async def add_movie_start(message: types.Message):

    if message.from_user.id != ADMIN:
        return

    await message.answer("🎬 Kino nomini yozing")
    await AddMovie.name.set()


# KINO NOMI
@dp.message_handler(state=AddMovie.name)
async def movie_name(message: types.Message, state: FSMContext):

    await state.update_data(name=message.text)

    await message.answer("📂 Kategoriya yozing")

    await AddMovie.category.set()


# KATEGORIYA
@dp.message_handler(state=AddMovie.category)
async def movie_category(message: types.Message, state: FSMContext):

    await state.update_data(category=message.text)

    await message.answer("🎥 Endi kinoni video qilib yuboring")

    await AddMovie.video.set()


# VIDEO QABUL QILISH
@dp.message_handler(content_types=['video'], state=AddMovie.video)
async def movie_video(message: types.Message, state: FSMContext):

    data = await state.get_data()

    name = data["name"]
    category = data["category"]

    file_id = message.video.file_id

    caption = f"""
🎬 {name}

📂 {category}
"""

    await add_movie(name, category, file_id, caption)

    await message.answer("✅ Kino bazaga qo‘shildi")

    await state.finish()


# KINO ID ORQALI KO‘RISH
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


# QIDIRUV
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

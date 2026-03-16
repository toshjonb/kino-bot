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
    post = State()


# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("🎬 Kino bot\n\nKino nomi yoki kodini yozing")


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

    await message.answer("📢 Endi kinoni kanalga yuklang va post linkini yuboring")

    await AddMovie.post.set()


# POST LINK QABUL QILISH
@dp.message_handler(state=AddMovie.post)
async def movie_post(message: types.Message, state: FSMContext):

    data = await state.get_data()

    name = data["name"]
    category = data["category"]

    try:
        link = message.text
        message_id = int(link.split("/")[-1])

    except:
        await message.answer("❌ Post link noto‘g‘ri")
        return

    await add_movie(name, category, message_id)

    await message.answer("✅ Kino bazaga qo‘shildi")

    await state.finish()


# KINO ID ORQALI KO‘RISH
@dp.message_handler(lambda message: message.text.isdigit())
async def movie_code(message: types.Message):

    movie = await get_movie_by_id(message.text)

    if not movie:
        await message.answer("❌ Kino topilmadi")
        return

    await bot.forward_message(
        message.chat.id,
        CHANNEL,
        movie[3]
    )

    await add_view(movie[0])


# QIDIRUV
@dp.message_handler()
async def search(message: types.Message):

    movies = await search_movie(message.text)

    if not movies:
        await message.answer("❌ Kino topilmadi")
        return

    text = "🎬 Topilgan kinolar\n\n"

    for m in movies:
        text += f"{m[0]}. {m[1]}\n"

    await message.answer(text)


async def on_startup(dp):
    await create_db()


executor.start_polling(dp, on_startup=on_startup)

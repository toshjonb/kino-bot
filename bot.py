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
"""
    )

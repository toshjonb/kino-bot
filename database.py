async def get_movie_by_id(movie_id):

    async with aiosqlite.connect(DB) as db:

        cursor = await db.execute(
            "SELECT * FROM movies WHERE id=?",
            (movie_id,)
        )

        movie = await cursor.fetchone()

        return movie

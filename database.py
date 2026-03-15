import aiosqlite

DB = "movies.db"


async def create_db():

    async with aiosqlite.connect(DB) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            file_id TEXT,
            views INTEGER DEFAULT 0
        )
        """)

        await db.commit()


async def get_movie_by_id(movie_id):

    async with aiosqlite.connect(DB) as db:

        cursor = await db.execute(
            "SELECT * FROM movies WHERE id=?",
            (movie_id,)
        )

        movie = await cursor.fetchone()

        return movie


async def add_view(movie_id):

    async with aiosqlite.connect(DB) as db:

        await db.execute(
            "UPDATE movies SET views = views + 1 WHERE id=?",
            (movie_id,)
        )

        await db.commit()


async def top_movies():

    async with aiosqlite.connect(DB) as db:

        cursor = await db.execute(
            "SELECT * FROM movies ORDER BY views DESC LIMIT 10"
        )

        movies = await cursor.fetchall()

        return movies

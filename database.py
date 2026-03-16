import aiosqlite

DB = "movies.db"


async def create_db():

    async with aiosqlite.connect(DB) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            message_id INTEGER,
            views INTEGER DEFAULT 0
        )
        """)

        await db.commit()


async def add_movie(name, category, message_id):

    async with aiosqlite.connect(DB) as db:

        await db.execute(
            "INSERT INTO movies(name,category,message_id) VALUES(?,?,?)",
            (name, category, message_id)
        )

        await db.commit()


async def search_movie(name):

    async with aiosqlite.connect(DB) as db:

        cursor = await db.execute(
            "SELECT * FROM movies WHERE name LIKE ?",
            (f"%{name}%",)
        )

        movies = await cursor.fetchall()

        return movies


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

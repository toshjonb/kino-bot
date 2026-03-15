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
            views INTEGER
        )
        """)

        await db.commit()

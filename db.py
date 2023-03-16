from datetime import date, timedelta
import sqlite3
from aiogram import Bot
import config
import os
import aiogram

bot = Bot(config.TOKEN)


class BotDB(aiogram.types.Message):
    def __init__(self):
        super().__init__()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.BASE_DIR, "db.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    async def create_table(self):
        self.conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    follower BOLLEAN DEFAULT 0,
    join_date DATETIME DEFAULT ((DATETIME('now'))) NOT NULL,
    follow_date DATETIME NOT NULL DEFAULT ((DATETIME('now'))),
    follow_end_date DATITIME,
    symbol INTEGER  DEFAULT 2000,
    drop_symbol_date DATETIME
    );""")
        return self.conn.commit()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute("SELECT id FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, user_name):
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?,?)", (user_id, user_name))
        return self.conn.commit()

    async def rename(self, user_name, user_id):
        self.cursor.execute("UPDATE users SET user_name = ? WHERE user_id = ?", (user_name, user_id))
        return self.conn.commit()

    async def buy_follow(self, user_id):
        current_date = date.today()
        days_follow = timedelta(days=31)
        result = current_date + days_follow
        self.cursor.execute("UPDATE users SET follower = ? WHERE user_id = ?", (1, user_id))
        self.cursor.execute("UPDATE users SET follow_date = ? WHERE user_id = ?", (current_date, user_id))
        self.cursor.execute("UPDATE users SET follow_end_date = ? WHERE user_id = ?", (result, user_id))
        return self.conn.commit()

    async def follower_exists(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE user_id = ? AND follower = ?",
                                     (user_id, 1))
        return bool(result.fetchall())

    async def follow_end_date_exists(self, user_id):
        current_date = date.today()
        result = self.cursor.execute(
            "SELECT * FROM users WHERE user_id = ? AND follow_end_date <= ?",
            (user_id, current_date))
        return bool(result.fetchall())

    async def drop_follow(self, user_id):
        self.cursor.execute("UPDATE users SET follower = ? WHERE user_id = ?", (0, user_id))
        return self.conn.commit()

    async def symbol(self):
        symbol_up = 2000
        self.cursor.execute("UPDATE users SET symbol = ?", (symbol_up,))
        return self.conn.commit()

    async def symbol_update(self, user_id, lention):
        self.cursor.execute("UPDATE users SET symbol = symbol - ? WHERE user_id = ?",
                            (lention, user_id))
        return self.conn.commit()

    async def symbol_exists(self, user_id, message):
        result = self.cursor.execute("SELECT symbol FROM users WHERE user_id = ?", (user_id,))
        return ' '.join(map(str, result.fetchall()[0]))

    async def symbol_exists_counter(self, user_id):
        result = self.cursor.execute("SELECT symbol FROM users WHERE user_id = ?", (user_id,))
        return int(' '.join(map(str, result.fetchall()[0])))

    async def symbol_date_update(self):
        current_date = date.today()
        days_follow = timedelta(days=1)
        result_day = current_date + days_follow
        self.cursor.execute("UPDATE users SET drop_symbol_date= ?",
                            (result_day,))
        return self.conn.commit()

    async def symbol_date(self):
        current_date = date.today()
        result = self.cursor.execute("SELECT drop_symbol_date FROM users WHERE drop_symbol_date <= ?", (current_date,))
        return bool(result.fetchall())

    async def create_symbol_date(self):
        current_date = date.today()
        days_follow = timedelta(days=1)
        result_day = current_date + days_follow
        self.cursor.execute("UPDATE users SET drop_symbol_date= ?",
                            (result_day,))
        return self.conn.commit()

    async def get_table(self, message):
        result = self.cursor.execute("SELECT * FROM users WHERE follower")
        await bot.send_message(message.chat.id, ' '.join(map(str, result.fetchall())))

    async def get_date_start(self, user_id):
        result = self.cursor.execute("SELECT join_date FROM users WHERE user_id = ?", (user_id,))
        return ' '.join(map(str, result.fetchone()))

    async def get_date_update(self, user_id):
        result = self.cursor.execute("SELECT drop_symbol_date FROM users WHERE user_id = ?", (user_id,))
        return ' '.join(map(str, result.fetchone()))

    async def get_date_end_follow(self, user_id):
        result = self.cursor.execute("SELECT follow_end_date FROM users WHERE user_id = ?", (user_id,))
        return ' '.join(map(str, result.fetchone()))

    def close(self):
        self.conn.close()

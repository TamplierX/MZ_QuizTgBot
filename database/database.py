import sqlite3 as sq
import logging


logger = logging.getLogger(__name__)


async def db_start():
    try:
        db = sq.connect('tg.db')
        cur = db.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                quiz_completed INTEGER,
                last_result TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ask (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                create_date TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                create_date TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL
            )
        ''')
        db.commit()
        db.close()
        logging.info("Database initialized successfully")
    except sq.Error as e:
        logger.error(f"Database initialization error: {e}")


async def add_user_db(user_id, username, quiz_completed=0, last_result='-Пусто-'):
    try:
        db = sq.connect('tg.db')
        cur = db.cursor()
        user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not user.fetchone():
            cur.execute("INSERT INTO users (user_id, username, quiz_completed, last_result) VALUES (?, ?, ?, ?)",
                        (user_id, username, quiz_completed, last_result))
            db.commit()
            logger.info(f"[Database.add_user] User added: {user_id} successfully")
        db.close()
    except sq.Error as e:
        logger.error(f"[Database.add_user {user_id}] - error: {e}")
    except Exception as e:
        logger.error(f"[Database.add_user {user_id}] - Unexpected error: {e}")


async def get_user_info(user_id):
    try:
        db = sq.connect('tg.db')
        cur = db.cursor()
        user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        db.close()
        return user
    except sq.Error as e:
        logger.error(f"[Database.get_user from User {user_id}] - error: {e}")
    except Exception as e:
        logger.error(f"[Database.get_user from User {user_id}] - Unexpected error: {e}")


async def upd_user_db(user_id, last_result):
    try:
        db = sq.connect('tg.db')
        cur = db.cursor()
        user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        cur.execute("UPDATE users SET quiz_completed = ? WHERE user_id = ?",
                    (user[3] + 1, user_id))
        cur.execute("UPDATE users SET last_result = ? WHERE user_id = ?",
                    (last_result, user_id))
        db.commit()
        db.close()
        logger.info(f"User {user_id} information updated successfully")
    except sq.Error as e:
        logger.error(f"[Database.upd_user {user_id}] - error: {e}")
    except Exception as e:
        logger.error(f"[Database.upd_user {user_id}] - Unexpected error: {e}")


async def add_ask_db(create_date, user_id, message):
    try:
        db = sq.connect('tg.db')
        cur = db.cursor()
        cur.execute("INSERT INTO ask (create_date, user_id, message) VALUES (?, ?, ?)",
                    (create_date, user_id, message))
        db.commit()
        db.close()
        logger.info(f"User {user_id} add ask successfully")
    except sq.Error as e:
        logger.error(f"[Database.add_ask from User {user_id}] - error: {e}")
    except Exception as e:
        logger.error(f"[Database.add_ask from User {user_id}] - Unexpected error: {e}")


async def add_feedback_db(create_date, user_id, message):
    try:
        db = sq.connect('tg.db')
        cur = db.cursor()
        cur.execute("INSERT INTO feedback (create_date, user_id, message) VALUES (?, ?, ?)",
                    (create_date, user_id, message))
        db.commit()
        db.close()
        logger.info(f"User {user_id} add feedback successfully")
    except sq.Error as e:
        logger.error(f"[Database.add_feedback from User {user_id}] - error: {e}")
    except Exception as e:
        logger.error(f"[Database.add_feedback from User {user_id}] - Unexpected error: {e}")

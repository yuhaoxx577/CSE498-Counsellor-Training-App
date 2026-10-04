import hashlib
import secrets
import sqlite3

DB_PATH = "counsellor_training.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        100000
    ).hex()


def register_user(username, password):
    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    try:
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                (username, salt, password_hash)
            )
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate_user(username, password):
    with get_connection() as connection:
        user = connection.execute(
            "SELECT id, salt, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    if user is None:
        return None

    user_id, salt, stored_hash = user
    entered_hash = hash_password(password, salt)

    if secrets.compare_digest(entered_hash, stored_hash):
        return user_id

    return None


import sqlite3

DB_PATH = "counsellor_training.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_patient_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                age_group TEXT NOT NULL,
                ethnicity TEXT NOT NULL,
                concern TEXT NOT NULL,
                summary TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)


def create_patient(
    user_id,
    name,
    gender,
    age_group,
    ethnicity,
    concern
):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO patients (
                user_id,
                name,
                gender,
                age_group,
                ethnicity,
                concern
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                name,
                gender,
                age_group,
                ethnicity,
                concern
            )
        )
        return cursor.lastrowid


def get_patients(user_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM patients
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,)
        ).fetchall()


def get_patient(patient_id, user_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT *
            FROM patients
            WHERE id = ? AND user_id = ?
            """,
            (patient_id, user_id)
        ).fetchone()


def update_patient_summary(patient_id, summary):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE patients
            SET summary = ?
            WHERE id = ?
            """,
            (summary, patient_id)
        )


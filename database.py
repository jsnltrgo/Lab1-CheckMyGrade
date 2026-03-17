import sqlite3
import os

os.makedirs('data', exist_ok=True)

def get_connection():
    conn = sqlite3.connect('data/checkmygrade.db')
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY NOT NULL,
            course_name TEXT NOT NULL,
            credits INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professors (
            professor_id TEXT PRIMARY KEY NOT NULL,
            professor_name TEXT NOT NULL,
            rank TEXT,
            course_id TEXT,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            email_address TEXT PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            course_id TEXT,
            grade TEXT,
            marks REAL,
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            grade_id TEXT PRIMARY KEY NOT NULL,
            grade TEXT NOT NULL,
            marks_min REAL NOT NULL,
            marks_max REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login (
            user_id TEXT PRIMARY KEY NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
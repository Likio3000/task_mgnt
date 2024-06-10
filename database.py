import sqlite3
import logging

DATABASE_NAME = 'schedule.db'

def connect_db():
    return sqlite3.connect(DATABASE_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        reward TEXT
    )''')
    conn.commit()
    conn.close()

def add_activity_to_db(title, description, start_time, end_time, reward):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO activities (title, description, start_time, end_time, reward)
            VALUES (?, ?, ?, ?, ?)''', (title, description, start_time, end_time, reward))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()

def get_activities_from_db(date=None):
    conn = connect_db()
    cursor = conn.cursor()
    if date:
        cursor.execute('SELECT * FROM activities WHERE DATE(start_time) = ? ORDER BY id DESC', (date,))
    else:
        cursor.execute('SELECT * FROM activities ORDER BY id DESC')
    activities = cursor.fetchall()
    conn.close()
    return activities

def delete_activity_from_db(activity_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        conn.close()

import sqlite3
import time

# Создаем или подключаемся к базе данных
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создаем таблицу users, если она еще не создана
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    tg_id TEXT PRIMARY KEY,
    time_sub INTEGER
)
''')

conn.commit()

# Функция для добавления нового пользователя
def add_user(tg_id):
    if not user_exists(tg_id):
        cursor.execute('INSERT INTO users (tg_id, time_sub) VALUES (?, ?)', (tg_id, 0))
        conn.commit()
        print(f"User with tg_id {tg_id} added to the database.")
    else:
        print(f"User with tg_id {tg_id} already exists in the database.")

# Функция для проверки, существует ли пользователь в базе
def user_exists(tg_id):
    cursor.execute('SELECT 1 FROM users WHERE tg_id = ?', (tg_id,))
    return cursor.fetchone() is not None

# Функция для получения значения time_sub по tg_id
def get_sub_status(tg_id):
    cursor.execute('SELECT time_sub FROM users WHERE tg_id = ?', (tg_id,))
    result = cursor.fetchone()
    time_sub = result[0]
    if time_sub > int(time.time()):
        return True
    else:
        return False
    
# Функция для обновления значения time_sub по tg_id
def set_time_sub(tg_id, time_sub):
    cursor.execute('UPDATE users SET time_sub = ? WHERE tg_id = ?', (time_sub, tg_id))
    conn.commit()

def get_all_tg_ids():
    cursor.execute('SELECT tg_id FROM users')
    result = cursor.fetchall()
    return [row[0] for row in result]
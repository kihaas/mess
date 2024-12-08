import sqlite3

def setup_database():
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('messenger.db')
    cursor = conn.cursor()

    # Создание таблицы пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL
        )
    ''')

    # Создание таблицы сообщений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    ''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
    print("База данных настроена успешно!")

if __name__ == "__main__":
    setup_database()

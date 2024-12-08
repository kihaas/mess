'''import psycopg2
from psycopg2 import sql

# Подключение к базе данных
def get_connection():
    return psycopg2.connect(
        dbname="message",
        user="postgres",
        password="1",
        host="localhost",
        port="5432"
    )

# Функция для регистрации пользователя
def register_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Проверка на существование пользователя
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return {"error": "Пользователь с таким логином уже существует"}

        # Регистрация пользователя
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        return {"message": "Регистрация успешна!"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()
'''
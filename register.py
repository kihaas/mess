from flask import request, jsonify, redirect, url_for, session
import sqlite3
import hashlib

DB_PATH = 'messenger.db'  # Путь к базе данных SQLite

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Регистрация пользователя
def process_register():
    # Получение данных из запроса
    data = request.form
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Проверка на заполнение полей
    if not username or not password or not confirm_password:
        return jsonify({"error": "Все поля обязательны"}), 400

    # Проверка длины пароля
    if len(password) < 6:
        return jsonify({"error": "Пароль должен быть не менее 6 символов"}), 400

    # Проверка совпадения пароля
    if password != confirm_password:
        return jsonify({"error": "Пароли не совпадают"}), 400

    try:
        # Подключение к базе данных SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Проверка уникальности имени пользователя
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return jsonify({"error": "Пользователь с таким логином уже существует"}), 400

        # Добавление нового пользователя
        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()

        # Получение ID зарегистрированного пользователя
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = cursor.fetchone()[0]

        # Установка сессии
        session['user_id'] = user_id

        return redirect(url_for('chat'))  # Перенаправление на маршрут /chats
    except sqlite3.Error as e:
        return jsonify({"error": f"Ошибка базы данных: {e}"}), 500
    finally:
        conn.close()

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def setup_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messenger.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)

    # Модель для пользователя
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)

    # Модель для сообщений
    class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        content = db.Column(db.Text, nullable=False)

    with app.app_context():
        db.create_all()

    # Главная страница
    @app.route("/")
    def index():
        if 'user_id' in session:
            return redirect(url_for('chat'))
        return render_template("index.html")

    # Регистрация
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            hashed_password = generate_password_hash(password)

            if User.query.filter_by(username=username).first():
                return "Пользователь с таким именем уже существует."

            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("login"))
        return render_template("register.html")

    # Логин
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect(url_for("chat"))  # Перенаправление в /chat
            return "Неверные данные для входа."
        return render_template("login.html")

    # Чат
    @app.route("/chat", methods=["GET", "POST"])
    def chat():
        if "user_id" not in session:
            return redirect(url_for("login"))

        user_id = session["user_id"]
        users = User.query.filter(User.id != user_id).all()
        messages = None

        if request.method == "POST":
            receiver_id = request.form["receiver_id"]
            content = request.form["content"]
            new_message = Message(sender_id=user_id, receiver_id=receiver_id, content=content)
            db.session.add(new_message)
            db.session.commit()

        messages = (
            Message.query.filter_by(receiver_id=user_id)
            .order_by(Message.id.desc())
            .all()
        )
        return render_template("chat.html", users=users, messages=messages)

    # Выход
    @app.route("/logout")
    def logout():
        session.pop("user_id", None)
        return redirect(url_for("index"))

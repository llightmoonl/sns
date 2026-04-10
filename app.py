from flask import Flask, jsonify, session, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from keras.models import load_model
import numpy as np
from PIL import Image
from datetime import timedelta
from flask_caching import Cache
import os
from functools import wraps

app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=1)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True

cache = Cache(config={"CACHE_TYPE": "simple"})
cache.init_app(app)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

model = load_model("mnist_model.h5")

@app.route("/")
def index():
    logged_in = session.get("logged_in", False)
    return render_template("index.html", logged_in=logged_in)

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for("registration"))
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("registration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["logged_in"] = True
            return render_template("index.html")
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

questions = [
    {
        "question": "Что такое сверточная нейронная сеть (СНС)?",
        "options": [
            "a) Модель, использующая только полносвязные слои для классификации",
            "b) Класс нейросетей, выделяющих иерархические признаки с помощью сверток",
            "c) Алгоритм оптимизации для обучения линейных моделей",
            "d) Метод сжатия изображений с потерями качества"
        ],
        "correct": 1,
        "topic": "Определение сверточной нейронной сети"
    },
    {
        "question": "Какие слои присутствуют в сверточной нейронной сети (СНС)?",
        "options": [
            "a) InputLayer, Dropout, Embedding",
            "b) LSTM, GRU, Bidirectional",
            "c) Conv2D, MaxPooling2D, Flatten, Dense",
            "d) GlobalAveragePooling2D, BatchNormalization, Reshape"
        ],
        "correct": 2,
        "topic": "Архитектура сверточной нейронной сети"
    },
    {
        "question": "В чем заключается главное свойство слоя Conv2D?",
        "options": [
            "a) Применяет рекурсивные операции к последовательностям данных",
            "b) Преобразует данные в одномерный массив",
            "c) Группирует признаки путем усреднения значений",
            "d) Применяет сверточные операции к поступившим в него данным"
        ],
        "correct": 3,
        "topic": "Архитектура сверточной нейронной сети"
    },
    {
        "question": "В чем заключается главное свойство слоя MaxPooling2D?",
        "options": [
            "a) Уменьшает размерность пространственных данных",
            "b) Проводит линейную регрессию над признаками",
            "c) Генерирует случайные числа для увеличения вариативности данных",
            "d) Складывает элементы матрицы"
        ],
        "correct": 0,
        "topic": "Архитектура сверточной нейронной сети"
    },
    {
        "question": "В чем заключается главное свойство слоя Flatten?",
        "options": [
            "a) Объединяет два слоя в один",
            "b) Производит масштабирование данных",
            "c) Накладывает фильтры на изображения",
            "d) Преобразует многомерные данные в одномерные"
        ],
        "correct": 3,
        "topic": "Архитектура сверточной нейронной сети"
    },
    {
        "question": "В чем заключается главное свойство слоя Dense?",
        "options": [
            "a) Удаляет лишние веса из предыдущей структуры",
            "b) Обрабатывает признаки, которые были извлечены из предыдущих слоев, а также генерирует выходные данные",
            "c) Разделяет пространство признаков на отдельные группы",
            "d) Преобразует категориальные значения в численные"
        ],
        "correct": 1,
        "topic": "Архитектура сверточной нейронной сети"
    },
    {
        "question": "Что такое функция активации в сверточной нейронной сети (СНС)?",
        "options": [
            "a) Способ хранения весов нейронов",
            "b) Метод оптимизации гиперпараметров",
            "c) Математическая функция, принимающая на вход определенное значение и преобразующая его в выходное значение",
            "d) Алгоритм нормализации данных"
        ],
        "correct": 2,
        "topic": "Функции активации сверточной нейронной сети"
    },
    {
        "question": "Какое предназначение у функции активации ReLU?",
        "options": [
            "a) Предназначена для введения нелинейности в нейронную сеть",
            "b) Предназначена исключительно для бинарной классификации",
            "c) Предназначена только для полносвязанных сетей",
            "d) Предназначена для удаления шума из данных"
        ],
        "correct": 0,
        "topic": "Функции активации сверточной нейронной сети"
    },
    {
        "question": "Какое предназначение у функции активации Softmax?",
        "options": [
            "a) Предназначена для повышения точности алгоритмов кластеризации",
            "b) Предназначена для сжатия размера изображений",
            "c) Предназначены для работы только с целыми числами",
            "d) Предназначена для преобразования вектора исходных чисел в вектор вероятностей"
        ],
        "correct": 3,
        "topic": "Функции активации сверточной нейронной сети"
    },
    {
        "question": "Какой порядок слоев должен быть у сверточной нейронной сети (СНС) для классификации цифр?",
        "options": [
            "a) Dense - Conv2D - Flatten - MaxPooling2D - Conv2D - Dense - MaxPooling2D",
            "b) Flatten - Dense - Conv2D - MaxPooling2D - Conv2D - MaxPooling2D - Dense",
            "c) MaxPooling2D - Conv2D - Dense - Flatten - MaxPooling2D - Conv2D - Dense",
            "d) Conv2D - MaxPooling2D - Conv2D - MaxPooling2D - Flatten - Dense - Dense"
        ],
        "correct": 3,
        "topic": "Архитектура сверточной нейронной сети"
    }
]

@app.route("/api/questions")
def get_questions():
    return jsonify(questions)

@app.route("/zadanie1")
@login_required
def zadanie1():
    return render_template("zadanie1.html")

CORRECT_ORDERS = [
    [4756, 1235, 5999, 3568, 5542, 1865, 4849, 3422, 1029],
    [4756, 1235, 5542, 3568, 5999, 1865, 4849, 3422, 1029]
]

@app.route("/zadanie2")
@login_required
def zadanie2():
    return render_template("zadanie2.html")

@app.route("/zadanie2/check_order", methods=["POST"])
def check_order():
    try:
        current_order = request.json["order"]
        for order in CORRECT_ORDERS:
            if len(order) != len(current_order):
                continue
            if all(val == current_order[i] for i, val in enumerate(order)):
                return jsonify({"result": True})
        return jsonify({"result": False})
    except Exception as e:
        print(f"Error checking order: {e}")
        return jsonify({"result": None}), 500

@app.route("/zadanie3", methods=["GET", "POST"])
@login_required
def zadanie3():
    digit = None
    image_url = None
    if request.method == "POST":
        if "image" not in request.files:
            digit = "Ошибка: изображение не загружено"
        else:
            file = request.files["image"]
            filename = file.filename
            save_path = os.path.join("static/images", filename)
            file.save(save_path)
            img = Image.open(save_path).convert("L").resize((28, 28))
            img = np.array(img) / 255.0
            img = img.reshape(1, 28, 28, 1)
            img = 1 - img
            prediction = model.predict([img])
            digit = np.argmax(prediction, axis=1)[0]
            image_url = url_for("static", filename=f"images/{filename}")
    return render_template("zadanie3.html", digit=digit, image_url=image_url)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("page404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
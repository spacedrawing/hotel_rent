import json
import os
from flask import Flask, render_template, url_for, session
from flask import request, redirect, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from data.hotel import Hotel
from data.review import Review
from data.user import User
from data import db_session
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=30)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth"


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(int(user_id))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    list_hotel_cards = [i.__dict__ for i in db_sess.query(Hotel).all()]

    for slov in list_hotel_cards:
        reviews = [
            i.__dict__
            for i in db_sess.query(Review).filter(Review.hotel_id == slov["id"]).all()
        ]
        if len(reviews) == 0:
            slov["rating"] = "Нет отзывов"
        else:
            slov["rating"] = str(sum(i["rating"] for i in reviews) / len(reviews))

    return render_template("index.html", list_hotel_cards=list_hotel_cards)


@app.route("/auth")
def auth_page():
    return render_template("auth.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == request.form["email"]).first():
        return "Пользователь уже существует"
    user = User(
        name=request.form["name"],
        surname=request.form["surname"],
        email=request.form["email"],
        patronymic=request.form["patronymic"],
        hashed_password=generate_password_hash(request.form["password"]),
    )
    db_sess.add(user)
    db_sess.commit()
    session["user_id"] = user.id
    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == request.form.get("email")).first()
    if not user or not check_password_hash(
        user.hashed_password, request.form.get("password")
    ):
        return render_template(
            "error.html",
            message="Неверный логин или пароль",
            retry_url=url_for("auth_page"),
        )

    login_user(user)
    return redirect("/")


@app.route("/hotel_menu/<index_hotel>")
def hotel_menu(index_hotel):
    db_sess = db_session.create_session()
    files = os.listdir(path="static/images_1")
    images = [
        url_for("static", filename=f"images_{index_hotel}/room{i}.jpg")
        for i in range(1, len(files) + 1)
    ]
    hotel_card = db_sess.query(Hotel).filter(Hotel.id == index_hotel).first().__dict__
    conveniences = hotel_card["conveniences"].split(";")
    reviews = [
        i.__dict__
        for i in db_sess.query(Review).filter(Review.hotel_id == index_hotel).all()
    ]
    return render_template(
        "hotel_menu.html",
        images=images,
        index_hotel=index_hotel,
        hotel_card=hotel_card,
        conveniences=conveniences,
        reviews=reviews,
    )


def main():
    db_session.global_init("db/hotel_data.sqlite")
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == "__main__":
    main()

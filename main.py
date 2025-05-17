import os
from flask import Flask, render_template, url_for
from flask import request, redirect
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
from data.room import Room
from data.booking import Booking
from data import db_session
from datetime import timedelta
from datetime import datetime as dt

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


@app.route("/", methods=["POST", "GET"])
def index():
    db_sess = db_session.create_session()
    list_hotel_cards = [i.__dict__ for i in db_sess.query(Hotel).all()]

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            return redirect(url_for("search") + f"?city={city}")

    for slov in list_hotel_cards:
        reviews = [i.__dict__ for i in db_sess.query(Review).filter(Review.hotel_id == slov["id"]).all()]
        if len(reviews) == 0:
            slov["rating"] = "Нет отзывов"
        else:
            slov["rating"] = round(sum(i["rating"] for i in reviews) / len(reviews), 1)

    return render_template("index.html", list_hotel_cards=list_hotel_cards)


@app.route("/search")
@login_required
def search():
    search_city = request.args.get("city")
    db_sess = db_session.create_session()
    hotels = db_sess.query(Hotel).filter(Hotel.city == search_city).all()

    hotel_cards = []
    for hotel in hotels:
        hotel_data = hotel.__dict__
        reviews = [i.__dict__ for i in db_sess.query(Review).filter(Review.hotel_id == hotel_data["id"]).all()]
        if len(reviews) == 0:
            hotel_data["rating"] = "Нет отзывов"
        else:
            hotel_data["rating"] = round(sum(i["rating"] for i in reviews) / len(reviews), 1)

        hotel_cards.append(hotel_data)

    return render_template("search.html", hotel_cards=hotel_cards, city = search_city)


@app.route("/auth")
def auth():
    return render_template("auth.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(User.email == request.form["email"]).first():
        return render_template(
            "error.html",
            message="Пользователь с таким email уже существует",
            retry_url=url_for("auth")
        )
    user = User(
        name=request.form["name"],
        surname=request.form["surname"],
        email=request.form["email"],
        patronymic=request.form["patronymic"],
        hashed_password=generate_password_hash(request.form["password"]),
    )
    db_sess.add(user)
    db_sess.commit()
    login_user(user)
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
            retry_url=url_for("auth"),
        )

    login_user(user)
    return redirect("/")


@app.route("/hotel_menu/<index_hotel>", methods=["GET", "POST"])
def hotel_menu(index_hotel):
    db_sess = db_session.create_session()

    if request.method == "POST":
        if current_user.is_authenticated:
            if request.form.get("review_button"):
                if request.form.get("rating"):
                    rating = int(request.form.get("rating"))
                else:
                    return render_template("error.html",
                                           message="Выберете количество звёзд для отзыва",
                                           retry_url=url_for("hotel_menu", index_hotel=index_hotel))

                new_review = Review(
                    text=request.form.get("text"),
                    rating=rating,
                    username=current_user.name,
                    user_id=current_user.id,
                    hotel_id=index_hotel,
                )
                db_sess.add(new_review)
                db_sess.commit()
                return redirect(f"/hotel_menu/{index_hotel}")

            elif request.form.get("booking_button"):
                date_out = request.form.get("checkout")
                date_in = request.form.get("checkin")
                if date_in and date_out:
                    date_out = dt.strptime(date_out, "%Y-%m-%d")
                    date_in = dt.strptime(date_in, "%Y-%m-%d")
                    if (date_in and date_out) and (date_in < date_out) and dt.now() < date_in and dt.now() < date_out:
                        booking_order = [i.__dict__ for i in
                                         db_sess.query(Booking).filter(Booking.room_id == request.form.get("room")).all()]
                        for i in booking_order:
                            if (dt.strptime(i["start_date"], "%Y-%m-%d") <= date_in <= dt.strptime(i["end_date"],
                                                                                                   "%Y-%m-%d")) or (
                                    dt.strptime(i["start_date"], "%Y-%m-%d") <= date_out <= dt.strptime(i["end_date"],
                                                                                                        "%Y-%m-%d")):
                                return render_template("error.html",
                                                       message="Эта дата уже занята попробуйте другую",
                                                       retry_url=url_for("hotel_menu", index_hotel=index_hotel))
                        new_booking = Booking(
                            room_id=request.form.get("room"),
                            user_id=1,
                            start_date=str(date_in).split()[0],
                            end_date=str(date_out).split()[0],
                        )
                        db_sess.add(new_booking)
                        db_sess.commit()
                        return redirect(f"/hotel_menu/{index_hotel}")
                    else:
                        return render_template("error.html",
                                               message="Корректно введите данные в поле с датой",
                                               retry_url=url_for("hotel_menu", index_hotel=index_hotel))
                else:
                    return render_template("error.html",
                                           message="Корректно введите данные в поле с датой",
                                           retry_url=url_for("hotel_menu", index_hotel=index_hotel))
        else:
            return redirect("/auth")

    room_types = [i.__dict__ for i in db_sess.query(Room).filter(Room.hotel_id == index_hotel).all()]
    files = os.listdir(path=f"static/images_{index_hotel}")
    images = [
        url_for("static", filename=f"images_{index_hotel}/room{i}.jpg")
        for i in range(1, len(files) + 1)
    ]
    hotel_card = db_sess.query(Hotel).filter(Hotel.id == index_hotel).first().__dict__
    conveniences = hotel_card["conveniences"].split(';')
    reviews = [i.__dict__ for i in db_sess.query(Review).filter(Review.hotel_id == index_hotel).all()]
    return render_template("hotel_menu.html", images=images, hotel_card=hotel_card,
                           conveniences=conveniences, reviews=reviews, room_types=room_types)


def main():
    db_session.global_init("db/hotel_data.sqlite")
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == "__main__":
    main()

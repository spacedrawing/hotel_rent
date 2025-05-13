import json
import os
from data import db_session
from flask import Flask, render_template, url_for
from data.hotel import Hotel
from data.review import Review

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    list_hotel_cards = [i.__dict__ for i in db_sess.query(Hotel).all()]

    for slov in list_hotel_cards:
        reviews = [i.__dict__ for i in db_sess.query(Review).filter(Review.hotel_id == slov["id"]).all()]
        if len(reviews) == 0:
            slov["rating"] = "Нет отзывов"
        else:
            slov["rating"] = str(sum(i["rating"] for i in reviews) / len(reviews))

    return render_template("index.html", list_hotel_cards=list_hotel_cards)


<<<<<<< HEAD
@app.route("/hotel_menu/<int:hotel_id>")
def hotel_menu(hotel_id):
    list_hotel_cards = [json.loads(i) for i in open('data/hotel_cards.txt', encoding="utf-8").read().split('\n') if i]
    hotel_data = next((h for h in list_hotel_cards if h['id'] == hotel_id), None)

    if not hotel_data:
        return "Hotel not found", 404

    files = os.listdir(path="static/images")
    images = [url_for('static', filename=f'images/room{i}.jpg') for i in range(1, len(files) + 1)]

    return render_template("hotel_menu.html", hotel=hotel_data, images=images)
=======
@app.route("/hotel_menu/<index_hotel>")
def hotel_menu(index_hotel):
    files = os.listdir(path="static/images_1")
    images = [url_for('static', filename=f'images_{index_hotel}/room{i}.jpg') for i in range(1, len(files) + 1)]

    return render_template("hotel_menu.html", images=images, index_hotel=index_hotel)
>>>>>>> 7316c23f2c468bc168c8dc4e6ef1e648dd88a58b


def main():
    db_session.global_init("db/hotel_data.sqlite")
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == "__main__":
    main()

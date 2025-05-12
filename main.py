import json
import os
from data import db_session
from flask import Flask, render_template, url_for
from data.hotel import Hotel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    list_hotel_cards = Hotel()
    list_hotel_cards = [json.loads(i) for i in open('data/hotel_cards.txt', encoding="utf-8").read().split('\n')]

    return render_template("index.html", list_hotel_cards=list_hotel_cards)


@app.route("/hotel_menu/<int:hotel_id>")
def hotel_menu(hotel_id):
    list_hotel_cards = [json.loads(i) for i in open('data/hotel_cards.txt', encoding="utf-8").read().split('\n') if i]
    hotel_data = next((h for h in list_hotel_cards if h['id'] == hotel_id), None)

    if not hotel_data:
        return "Hotel not found", 404

    files = os.listdir(path="static/images")
    images = [url_for('static', filename=f'images/room{i}.jpg') for i in range(1, len(files) + 1)]

    return render_template("hotel_menu.html", hotel=hotel_data, images=images)


def main():
    db_session.global_init("db/hotel_data.sqlite")
    app.run(host="127.0.0.1", port=8080, debug=True)


if __name__ == "__main__":
    main()

    db_sess = db_session.create_session()

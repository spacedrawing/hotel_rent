import json
import os
from data import db_session

from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    list_hotel_cards = [json.loads(i) for i in open('data/hotel_cards.txt', encoding="utf-8").read().split('\n')]
    return render_template("index.html", list_hotel_cards=list_hotel_cards)

@app.route("/hotel_menu")
def hotel_menu():
    files = os.listdir(path="static/images")
    images = [url_for('static', filename=f'images/room{i}.jpg') for i in range(1, len(files) + 1)]

    return render_template("hotel_menu.html", images=images)

def main():
    db_session.global_init("db/test0.sqlite")
    app.run(host="127.0.0.1", port=8080, debug=True)

if __name__ == "__main__":
    main()
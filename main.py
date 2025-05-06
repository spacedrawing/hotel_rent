from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hotel_menu")
def hotel_menu():
    images = [
        url_for('static', filename='images/room1.png'),
        url_for('static', filename='images/room2.jpg'),
        url_for('static', filename='images/room3.jpg'),
    ]
    return render_template("hotel_menu.html", images=images)

def main():
    app.run(host="127.0.0.1", port=8080, debug=True)

if __name__ == "__main__":
    main()
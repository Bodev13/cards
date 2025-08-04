from os import getenv
from crypt import methods
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
import dotenv
from bson.objectid import ObjectId

dotenv.load_dotenv()

app: Flask = Flask(__name__)
db_daten = getenv("MONGO_URI", default="mongodb://localhost:27017/cards_db")

print(f"{db_daten=}")
app.config['MONGO_URI'] = db_daten
mongo = PyMongo(app)


# @app.get("/cards")
@app.route("/cards", methods=['GET'])
def get_cards():
    # card_list: list[str] = ["As", "Karo", "Pik", "Dame", "Bub", "Kreuz"]
    cards = list(mongo.db.cards.find())
    return render_template("/cards.html", cards=cards)


@app.route("/cards/add_card_form", methods=["GET", "POST"])
def add_card_form():
    if request.method == "GET":
        print("Request is GET")
        return render_template("/add_card_form.html")

    elif request.method == "POST":
        print("Anfrage ist post")
        title = request.form.get("title")
        desc = request.form.get("desc")
        additional_desc = request.form.get("additional_desc")
        print(f"{title=} {desc=}")
        card = {
            "title": title,
            "description": desc,
            "additional_description": additional_desc,
            "created_at": datetime.now()

        }
        mongo.db.cards.insert_one(card)
        return redirect(url_for('get_cards'))

# f"select title from card where title like '{title_variable}%'


@app.get("/cards/<card_id>")
def update_card(card_id):
    card = mongo.db.cards.find_one({"_id": ObjectId(card_id)})
    if card is not None:
        print(f"{card=}")
        return jsonify(card)
    return f"Card not found", 404


@app.route("/cards/update/<card_id>", methods=["GET", "POST"])
def update_cards(card_id):
    if request.method == "GET":
        card = mongo.db.cards.find_one({"_id": ObjectId(card_id)})
        return render_template("cards_update.html", card=card)

    elif request.method == "POST":
        new_title = request.form.get("title")
        new_desc = request.form.get("desc")
        additional_desc = request.form.get("additional_desc")
        mongo.db.cards.update_one(
            {"_id": ObjectId(card_id)},
            {"$set": {
                "title": new_title,
                "description": new_desc,
                "additional_description": additional_desc
            }}
        )

    return redirect(url_for('get_cards'))


@app.route("/cards/delete/<card_id>", methods=["POST"])
def delete_card(card_id):
    mongo.db.cards.delete_one({"_id": ObjectId(card_id)})
    return redirect(url_for('get_cards'))


@app.route("/")
def home():
    return redirect(url_for("get_cards"))


tarot_cards = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World",
    # Wands
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands",
    "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands",
    "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands",
    # Cups
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups",
    "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups",
    "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",
    # Swords
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords",
    "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords",
    "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",
    # Pentacles
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles",
    "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles",
    "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles"
]


def create_cards():
    if mongo.db.cards.count_documents({}) > 0:
        print("Cards already exist, no more creating needed")
        return

    card_titles = []
    for title in tarot_cards:
        card = {
            "title": title,
            "description": "",
            "additional_description": "",
            "created_at": datetime.now()
        }
        card_titles.append(card)

    if card_titles:
        mongo.db.cards.insert_many(card_titles)
        print(f"Created {len(card_titles)} cards")


@app.route("/cards/reading", methods=["POST"])
def card_reading():
    selected_ids = request.form.getlist("card_ids")
    selected_cards = list(mongo.db.cards.find(
        {"_id": {"$in": [ObjectId(cid) for cid in selected_ids]}}))
    return render_template("reading_form.html", selected_cards=selected_cards)


# @app.route("/cards/reading/save", methods=["POST"])
# def save_reading():


if __name__ == "__main__":
    with app.app_context():
        mongo.db.cards.delete_many({})
        print("All cards deleted")
        create_cards()
    app.run("0.0.0.0", port=5001, debug=True)

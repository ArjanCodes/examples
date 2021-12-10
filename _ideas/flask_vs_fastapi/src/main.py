from dataclasses import dataclass
from datetime import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////hotel.db"
db = SQLAlchemy(app)


@dataclass
class User(db.Model):
    id: int
    email: str

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    email = db.Column(db.String(200), unique=True)


@app.route("/users/", strict_slashes=False)
def users():
    users = User.query.all()
    return jsonify(users)


@app.route("/user/<id>", methods=["POST"])
def read_user(id: str):
    print(id)
    print(request.json["room_id"])
    return "hello"


if __name__ == "__main__":
    users = User(email="user1@gmail.com"), User(email="user2@gmail.com")
    db.create_all()
    db.session.add_all(users)
    db.session.commit()
    app.run()

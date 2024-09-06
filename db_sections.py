from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = os.urandom(24)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(80), unique=True, nullable=False)
    game_link = db.Column(db.String(250), unique=False, nullable=False)
    game_description = db.Column(db.String(250), unique=False, nullable=False)

    def __str__(self):
        return f"Game Name:{self.game_name}, Game Link:{self.game_link}, Game Description:{self.game_description}"


class GameGeneralInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_manufacture = db.Column(db.String(80), unique=False, nullable=False)
    game_first_main_actor = db.Column(db.String(80), unique=False, nullable=False)
    game_second_main_actor = db.Column(db.String(80), unique=False, nullable=True)
    game_third_main_actor = db.Column(db.String(80), unique=False, nullable=True)
    game_fourth_main_actor = db.Column(db.String(80), unique=False, nullable=True)
    game_year_release = db.Column(db.Date(), unique=False, nullable=False)

    def __str__(self):
        return f"Game Manufacture:{self.game_manufacture}, Game First Main Actor:{self.game_first_main_actor}," \
               f" Game Second Main Actor:{self.game_second_main_actor}, " \
               f" Game Third Main Actor:{self.game_third_main_actor}," \
               f" Game Fourth Main Actor:{self.game_fourth_main_actor}," \
               f" Game Year Release:{self.game_year_release},"


class Note(db.Model):
    note_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, unique=False, nullable=False)
    note_text = db.Column(db.String(80), unique=False, nullable=True)

    def __str__(self):
        return f"Game id:{self.game_id}, Note:{self.note_text}"


with app.app_context():
    db.create_all()

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
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


@app.route('/')
def homepage():
    my_games_list = get_games_list()
    return render_template('homepage.html', games=my_games_list)


@app.route('/game_form', methods=['GET', 'POST'])
def add_game():
    if request.method == 'GET':
        return render_template("add_game.html")
    elif request.method == 'POST':
        add_new_game()

    return render_template('success.html')


@app.route('/delete_all_games', methods=['DELETE'])
def delete_all_games():
    try:
        num_rows_deleted = db.session.query(Game).delete()
        num_rows_deleted_game_info = db.session.query(GameGeneralInfo).delete()
        db.session.commit()
        return jsonify({"message": f"Deleted {num_rows_deleted} games"},
                       {"message": f"Deleted {num_rows_deleted_game_info} games info"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/<int:game_id>')
def show_game_general_info(game_id):
    games_general_info_list = get_games_general_info_list()
    current_game_info = games_general_info_list[game_id - 1]
    print(f"current_game: {current_game_info}")
    my_games_list = get_games_list()
    current_game = my_games_list[game_id - 1]
    return render_template('gamedetails.html', game=current_game, game_info=current_game_info)


@app.route('/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    try:
        # Query the game by ID
        print(f"Going to delete game with id:{game_id}")
        game_to_delete = db.session.query(Game).filter_by(id=game_id).first()
        game_info_to_delete = db.session.query(GameGeneralInfo).filter_by(id=game_id).first()

        # If the game exists, delete it
        if game_to_delete:
            db.session.delete(game_to_delete)
            db.session.commit()
            db.session.delete(game_info_to_delete)
            db.session.commit()
            print(f"Game with ID {game_id} has been deleted.")
        else:
            print(f"No game found with ID {game_id}.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")

    return jsonify({"message": f"Deleted Game with id: {game_id}"},
                   {"message": f"Deleted Game Info with id: {game_id}"}), 200


def get_games_list():
    my_games = Game.query.all()  # Query all games from the database
    print(f"My games: {my_games}")
    my_games_list = [
        {"id": game.id, "game_name": game.game_name, "game_link": game.game_link,
         "game_description": game.game_description} for game
        in my_games]
    print(f"My games list: {my_games_list}")
    return my_games_list


def get_games_general_info_list():
    my_games_general_info = GameGeneralInfo.query.all()  # Query all games general info from the database
    print(f"My games general info: {my_games_general_info}")
    my_games_general_info_list = [
        {"id": game_general_info.id, "game_manufacture": game_general_info.game_manufacture,
         "game_first_main_actor": game_general_info.game_first_main_actor,
         "game_second_main_actor": game_general_info.game_second_main_actor,
         "game_third_main_actor": game_general_info.game_third_main_actor,
         "game_fourth_main_actor": game_general_info.game_fourth_main_actor,
         "game_year_release": game_general_info.game_year_release} for game_general_info
        in my_games_general_info]
    print(f"My games general info list: {my_games_general_info_list}")
    return my_games_general_info_list


def add_new_game():
    game_name = request.form.get("game_name")
    game_link = request.form.get("game_link")
    game_description = request.form.get("game_description")
    new_game = Game(game_name=game_name, game_link=game_link, game_description=game_description)
    db.session.add(new_game)
    db.session.commit()
    game_manufacture = request.form.get("game_manufacture")
    game_main_actors = request.form.get("game_main_actors")
    game_main_actors_list = game_main_actors.split(",")
    game_year_release_string = request.form.get("game_year_release")
    game_year_release = datetime.strptime(game_year_release_string, "%Y").date()

    new_game_general_info = GameGeneralInfo(game_manufacture=game_manufacture,
                                            game_first_main_actor=game_main_actors_list[0],
                                            game_second_main_actor=game_main_actors_list[1],
                                            game_third_main_actor=game_main_actors_list[2],
                                            game_fourth_main_actor=game_main_actors_list[3],
                                            game_year_release=game_year_release)
    db.session.add(new_game_general_info)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)

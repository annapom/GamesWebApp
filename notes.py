from flask import request, render_template, jsonify
from datetime import datetime

from db_sections import Game, GameGeneralInfo, app, db, Note


# API Route to add a new note



def get_all_notes_list():
    my_notes = Note.query.all()
    print(f"Notes: {my_notes}")
    my_notes_list = [
        {"note_id": note.note_id, "game_id": note.game_id, "note_name": note.note_text}
        for note in my_notes]
    print(f"All Notes: {my_notes_list}")
    return my_notes_list


def get_game_notes_per_game_id(game_id):
    notes_list_for_specific_game = []
    notes_data = Note.query.where(Note.game_id == game_id).all()
    for note in notes_data:
        notes_list_for_specific_game.append(note.note_text)

    return notes_list_for_specific_game

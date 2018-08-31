import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('auth', __name__, url_prefix='/api')


@bp.route('/', methods=('GET', 'POST'))
def getData():
    if request.method == 'GET':
        d = {"name": "Zach", "id": "123456"}
        return jsonify(d)

@bp.route('/exercise/new-user', methods=['POST'])
def add_user():
    error = None
    if request.form['username'] == '':
        error = "Please provide a username!"
    else:
        return jsonify({"message": "You've added a user"})
    flash(error)
    return redirect(url_for('index'))

@bp.route('/exercise/add', methods=['POST'])
def add_exercises():
    errors = []
    if request.form["user-id"] == '':
        errors.append("Id please")
    if request.form['description'] == '':
        errors.append("no description provided")
    if request.form['duration'] == '':
        errors.append("no duration provided")
    if request.form['date'] == '':
        errors.append("no date provided")
    if not errors:
        return jsonify({"message": "You've added an exercise"})
    else:
        for error in errors:
            flash(error)
        return redirect(url_for('index'))
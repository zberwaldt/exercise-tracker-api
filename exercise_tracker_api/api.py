import functools
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from exercise_tracker_api.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/api')


@bp.route('/', methods=('GET', 'POST'))
def getData():
    if request.method == 'GET':
        d = {"name": "Zach", "id": "123456"}
        return jsonify(d)

@bp.route('/exercise/new-user', methods=['POST'])
def add_user():
    
    username = request.form['username']
    
    # Generate a special ID per user, from a uuid take only first 8 characters 
    # for brevity.
    user_id = str(uuid.uuid4())[:8]
    
    db = get_db()
    
    error = None
    if not username:
        error = "Please provide a username!"
    elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'user {} is already taken.'.format(username)
    
    if error is None:
        newEntry = db.cursor().execute(
            'INSERT INTO user (username, user_id) VALUES (?, ?)',
            (username, user_id)
        )
        db.commit()
        return jsonify({
            "username": username,
            "user_id": user_id
        })
    
    flash(error)
    
    return redirect(url_for('index'))

@bp.route('/exercise/add', methods=['POST'])
def add_exercises():
    # Get database so you can query it!
    db = get_db()

    user_id = request.form['user-id']
    description = request.form['description']
    duration = request.form['duration']
    date = request.form['date']

    errors = []
    exercise = {}

    # First check if ID is empty
    if user_id == '':
        # add relevant error
        errors.append("Id cannot be empty")
    # Now check to make sure the provided ID is present in the table
    elif db.execute(
        'SELECT id FROM user WHERE user_id = ?',
        (user_id,)
        ).fetchone() is None:
        errors.append("You did not enter a valid ID")
    else:
        exercise['user_id'] = user_id

    if description == '':
        errors.append("no description provided")
    else:
        exercise['description'] = description
    if duration == '':
        errors.append("no duration provided")
    else:
        exercise['duration'] = duration
    if date == '':
        errors.append("no date provided")
    else:
        exercise['date'] = date

    # If there IS NOT errors AND there IS an exercise
    if not errors and exercise:
        newEntry = db.cursor().execute(
            'INSERT INTO exercise (user_id, body, duration, date_of) VALUES (?, ?, ?, ?)',
            (user_id, description, duration, date)
        )
        db.commit()
        # return the json data of your new exercise
        return jsonify(exercise)
    else:
        for error in errors:
            flash(error)
        return redirect(url_for('index'))

@bp.route('/exercise/log', methods=['GET'])
def get_exercises():
    # Get database so you can query it!
    db = get_db()

    if not request.args.get('user_id'):        
        flash("You must provide an user_ID in your GET request")
        return redirect(url_for('index'))
    else:
        return jsonify({"message": "Route not fully implemented"})

# fc89411a jocko
# e29af261 zberwaldt
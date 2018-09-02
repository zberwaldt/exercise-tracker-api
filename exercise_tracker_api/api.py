import functools
import datetime
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
    elif None:
        pass
    else:
        exercise['duration'] = int(duration)
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
        
    # Get the user_id parameter from the request, because it is required.
    user_id = request.args.get('user_id')

    # create an array for errors
    errors = []

    # an array for holding params
    query_params = [user_id]

    # this are optional arguments to allow for more specific requests.
    from_date = request.args.get('from')
    # check to see if the from_date is truthy and is valid
    if from_date and validate(from_date):
        # if it is not, add to the errors array.
        errors.append("You did not provide a correct date")
    # otherwise, add the query to the params list.
    elif from_date is None:
        pass
    else:
        query_params.append(from_date)
    
    to_date = request.args.get('to')
    
    if to_date and not validate(to_date):
    
        errors.append("You did not provide a correct date")
    
    elif to_date is not None:
    
        query_params.append(from_date)
   
    limit = request.args.get('limit')
    
    # if there IS a limit but it's not an INT flash an error
    if limit and type(int(limit)) is not int:
    
        errors.append("Your limit parameter was not a integer")
    elif limit is None:
        pass
    # otherwise add it the params list.
    else:
    
        query_params.append(limit)
    
    # Also, create a query string 
    db_query = "SELECT e.user_id, body, duration, date_of, username FROM exercise e JOIN user u ON e.user_id = u.user_id WHERE e.user_id = ?"
    
    if from_date and not to_date:
    
        db_query += " AND date(date_of) >= date(?)"
    
    elif from_date and to_date:
    
        db_query += " BETWEEN date(?) AND date(?)"
    
    if limit:
        db_query += " LIMIT ?"

    print(db_query)
    print(query_params)
    # a user_id is required to request exercise data.
    if user_id is None:        
        flash("You must provide an user_ID in your GET request")    

    # also check to make sure the ID is valid. i.e. exists
    elif db.execute( 'SELECT id FROM user WHERE user_id = ?', (user_id,)).fetchone() is None:
        flash("No such user found. Please double check your spelling.")
        
    # Finally retrieve the data.
    else:
        user_exercises = db.cursor().execute(
            db_query,
            query_params
        ).fetchall()

    if user_exercises:
        exercise_data = []

        for exercise in user_exercises:
            newEntry = {
                'username': exercise['username'],
                'description': exercise['body'],
                'duration': exercise['duration'],
                'date': exercise['date_of'],
            }
            exercise_data.append(newEntry)
        
        return jsonify(exercise_data)
    else:
        flash("No entries found!")
    
    return redirect(url_for('index'))    
    
# fc89411a jocko
# e29af261 zberwaldt
# d95c4a62 kyleinapile
# 093d8745 timmytinkles

def validate(date_text):
    try: 
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    
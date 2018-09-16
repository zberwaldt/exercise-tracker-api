import functools
import datetime
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

# import login required decorator
from exercise_tracker_api.auth import login_required

# import access to database.
from exercise_tracker_api.db import get_db

# Define a blue print
bp = Blueprint('api', __name__, url_prefix='/api')

# This is a dumby route I need to remove.
@bp.route('/', methods=('GET', 'POST'))
def getData():
    if request.method == 'GET':
        d = {"name": "Zach", "id": "123456"}
        return jsonify(d)

# Define a route that is responsible for handling adding users to the database.
@bp.route('/exercise/new-user', methods=['POST'])
def add_user():
    
    username = request.form['username']
    
    # Generate a special ID per user, from a uuid take only first 8 characters 
    # for brevity. Although in hind sight this might be redundant. 
    # I got the idea from a node api I looked at briefly for reference.
    user_id = str(uuid.uuid4())[:8]
    
    # get the database
    db = get_db()
    
    # initialize error variable.
    error = None

    # if username is falsy
    if not username:
        # provide an error
        error = "Please provide a username!"

    # check to see if the username exists to prevent duplicates
    elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
        # if it does provide an error. 
        # I don't know why I formatted the error this way. I can't remember.
            error = f'user {username} is already taken.'
    
    # if there is no error
    if error is None:

        # create a new entry in teh database, I used cursor because originally 
        # I was going to use the row ID, and using cursor lets you get the 
        # last inserted id
        db.cursor().execute(
            'INSERT INTO user (username, user_id) VALUES (?, ?)',
            (username, user_id)
        )

        # commit to the database
        db.commit()

        # return the data as json, this is supposed to be like a microservice.
        return jsonify({
            "username": username,
            "user_id": user_id
        })
    
    # flash the error
    flash(error)
    
    # redirect to the index, I probably want to address this.
    return redirect(url_for('index'))

@bp.route('/exercise/add', methods=['GET', 'POST'])
def add_exercises():
    # Get database so you can query it!
    if request.method == 'GET':
        return render_template('api/add_exercise.html')
    else: 
        db = get_db()

        user_id = g.user['user_id']
        details = request.form['details']
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

        if details == '':
            errors.append("no details provided")
        else:
            exercise['details'] = details
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
            db.cursor().execute(
                'INSERT INTO exercise (user_id, details, duration, date_of) VALUES (?, ?, ?, date(?))',
                (user_id, details, duration, date)
            )
            db.commit()
            # return the json data of your new exercise
            return redirect(url_for('user.user_exercises', userid=g.user['user_id']))
            
        else:
            for error in errors:
                flash(error)
            return redirect(url_for('index'))

@bp.route('/exercise/<exerciseid>/delete', methods=['GET'])
@login_required
def delete_exercise(exerciseid):
    db = get_db()
    userid = g.user['user_id']
    db.execute(
        'DELETE FROM exercise WHERE id=?',
        (exerciseid,)
    )
    db.commit()
    flash('Exercise Deleted')
    return redirect(url_for('user.user_exercises', userid=userid))

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
    
    if to_date and validate(to_date):
    
        errors.append("You did not provide a correct date")
    
    elif to_date is None:
       
        pass
    
    else:
    
        query_params.append(to_date)
   
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
    db_query = "SELECT e.user_id, details, duration, date_of, username FROM exercise e JOIN user u ON e.user_id = u.user_id WHERE e.user_id = ?"
    
    if from_date and not to_date:
    
        db_query += " AND date(date_of) >= date(?)"
    
    elif from_date and to_date:
    
        db_query += " AND date(date_of) BETWEEN date(?) AND date(?)"
    
    if limit:
        db_query += " LIMIT ?"

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
                'details': exercise['details'],
                'duration': exercise['duration'],
                'date': exercise['date_of'],
            }
            exercise_data.append(newEntry)
        
        return jsonify(exercise_data)
    else:
        flash("No entries found!")
    
    return redirect(url_for('index'))    

@bp.route('/profile/add', methods=['GET','POST'])
def add_profile():
    if request.method == 'GET':
        print('No profile exists, let\'s create one')
        return render_template('user/create_profile.html')

    if request.method == 'POST':
        print('post request')
        db = get_db()

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        bio = request.form['bio']
        twitter = request.form['twitter']
        github = request.form['github']
        user_id = g.user['user_id']
        
        db.execute(
            'INSERT INTO profile (user_id,firstname, lastname, bio, twitter, github) VALUES (?,?,?,?,?,?)',
            (user_id, firstname, lastname, bio, twitter, github)
        )
        db.commit()

        print(user_id, firstname, lastname, bio, twitter, github)

        return redirect(url_for('user.user_profile', userid=user_id))

@bp.route('/user/<username>', methods=['GET'])
def get_userid(username):
    db = get_db()

    user = db.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()

    if user is None:
        flash("No user found.")
        redirect(url_for('index'))
    else:
        return jsonify({"username": user['username'], "user_id": user['user_id']})


@bp.route('/users', methods=['GET'])
def get_users():
    db = get_db()

    users = db.execute("SELECT * FROM user").fetchall()

    all_users = []

    for user in users:
        all_users.append({"username": user['username'], "user_id": user['user_id']})

    return jsonify(all_users)

    
# create a validate function that makes sure a date is a valid date. 
# It only returns false. if the Try is successful it doesn't return anything
# So that's something I want to address.
def validate(date_text):
    try: 
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    
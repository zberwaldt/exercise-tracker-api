import functools
import datetime
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, Response
)

# import login required decorator
from exercise_tracker_api.auth import login_required

# import access to database.
from exercise_tracker_api.db import get_db

# Define a blue print
bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/exercise/add', methods=['GET', 'POST'])
def add_exercises():
    
    """ /exercise/add is for using AJAX to add new exercises, instead of contantly redirecting to different pages. Will refactor to make it more secure. And only available to the current user. """
    
    # Get database so you can query it!
    if request.method == 'GET':
        return render_template('api/add_exercise.html')
    else: 
        db = get_db()

        userid = g.user['userid']
        details = request.form['details']
        duration = request.form['duration']
        date = request.form['date']

        errors = []
        exercise = {}

        # First check if ID is empty
        if userid == '':
            # add relevant error
            errors.append("Id cannot be empty")
        # Now check to make sure the provided ID is present in the table
        elif db.execute(
            'SELECT id FROM user WHERE userid = ?',
            (userid,)
            ).fetchone() is None:
            errors.append("You did not enter a valid ID")
        else:
            exercise['userid'] = userid

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
                'INSERT INTO exercise (userid, details, duration, date_of) VALUES (?, ?, ?, date(?))',
                (userid, details, duration, date)
            )
            db.commit()
            # return the json data of your new exercise
            return redirect(url_for('user.user_exercises', userid=g.user['userid']))
            
        else:
            for error in errors:
                flash(error)
            return redirect(url_for('index'))

@bp.route('/exercise/<exerciseid>/delete', methods=['POST'])
@login_required
def delete_exercise(exerciseid):

    """ Simple ajax route for deleting a exercise from the database for a user """


    db = get_db()
    userid = g.user['userid']
    db.execute(
        'DELETE FROM exercise WHERE id=?',
        (exerciseid,)
    )
    db.commit()
    flash('Exercise Deleted')
    return Response(status=200)

@bp.route('/exercise/<exerciseid>/edit', methods=('GET', 'POST'))
@login_required
def edit_exercise(exerciseid):

    """ Simple route for editing a given exercise record. """

    db = get_db()
    userid = g.user['userid']

    exercise_to_edit = db.execute(
        'SELECT * FROM exercise WHERE id=? AND userid=?',
        (exerciseid, userid)
    ).fetchone()

    return "Edit exercise."


@bp.route('/users', methods=['GET'])
@login_required
def get_users():

    """ Builds a list for all registered users on the site, so you can view their profiles and exercise logs. Currently under review. """

    db = get_db()

    users = db.execute("SELECT * FROM user").fetchall()

    all_users = []

    for user in users:
        all_users.append({"username": user['username'], "userid": user['userid']})

    return jsonify(all_users)


def validate(date_text):
    """
    A validate function that makes sure a date is a valid date.
    Only returns false, will return to make more complete.
    """

    try: 
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    
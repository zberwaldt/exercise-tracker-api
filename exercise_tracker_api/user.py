import functools
import datetime
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

# import access to database.
from exercise_tracker_api.db import get_db

# Define a blue print
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
def all_users():

    db = get_db()

    users = db.execute(
        'SELECT username FROM user',
    ).fetchall()

    return render_template('users/user_list.html', users=users)

# Define a route that is responsible for handling adding users to the database.
@bp.route('/<userid>/profile', methods=['GET', 'POST'])
def user_profile(userid):
    # get the database
    db = get_db()
    
    user = db.execute(
        'SELECT * FROM profile p JOIN user u ON  p.user_id = u.user_id WHERE p.user_id=?',
        (userid,)
    ).fetchone()

    print(user)
    


    if user is not None:
        return render_template('user/profile.html', user=user)
    elif g.user['user_id'] != userid:
        return render_template('user/profile.html', user=user)
    else:
        return redirect(url_for('api.add_profile'))

    # redirect to the index, I probably want to address this.
    return redirect(url_for('index'))


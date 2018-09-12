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
@bp.route('/<userid>/profile', methods=['GET'])
def user_profile(userid):

    # get the database
    db = get_db()
    
    user = db.execute(
        'SELECT username FROM user WHERE user_id=?',
        (userid,)
    ).fetchone() 
    
    if user is not None:
        return render_template('user/profile.html', user=user)
    else:
        flash('No user exists')

    # redirect to the index, I probably want to address this.
    return redirect(url_for('index'))


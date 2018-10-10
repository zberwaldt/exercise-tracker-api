import functools
import datetime
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)

# import login required decorator
from exercise_tracker_api.auth import login_required

# import access to database.
from exercise_tracker_api.db import get_db

# Define a blue print
bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
@login_required
def all_users():

    db = get_db()

    users = db.execute(
        'SELECT username, userid FROM user',
    ).fetchall()

    return render_template('user/user_list.html', users=users)

@bp.route('/<userid>/profile/edit', methods=('GET', 'POST'))
@login_required
def edit_profile(userid):
    db = get_db()
    if request.method == 'GET':
        if userid == g.user['userid']:
            
            user = db.execute(
                'SELECT * FROM user WHERE userid=?',
                (userid,)
            ).fetchone()
            return render_template('user/edit_profile.html', user=user)
        else:
            abort(401)
    else:
        bio = request.form['bio']
        twitter = request.form['twitter']
        facebook = request.form['facebook']
        instagram = request.form['instagram']

        dbquery = 'UPDATE user SET '
        dbparams = []

        if bio:
            dbquery += "bio = ?,"
            dbparams.append(bio)
        if twitter:
            dbquery += "twitter = ?,"
            dbparams.append(twitter)
        if facebook:
            dbquery += "facebook = ?,"
            dbparams.append(facebook)
        if instagram:
            dbquery += "instagram = ?"            
            dbparams.append(instagram)

        dbquery += ' WHERE userid = ?'
        dbparams.append(g.user['userid'])
        print(dbquery)
        print(dbparams)
        db.execute(
            dbquery,
            dbparams
        )
        db.commit()
        return redirect(url_for('user.user_profile', userid=g.user['userid']))

# Define a route that is responsible for handling adding users to the database.
@bp.route('/<userid>/profile', methods=['GET', 'POST'])
@login_required
def user_profile(userid):

    # get the database
    db = get_db()
    
    # user = db.execute(
    #     'SELECT * FROM profile p JOIN user u ON  p.userid = u.userid WHERE p.userid=?',
    #     (userid,)
    # ).fetchone()
    user = db.execute(
        'SELECT * FROM user WHERE userid=?',
        (userid,)
    ).fetchone()

    if user is None:
        return render_template('errors/404.html'), 404
    if user is not None or not g.user or g.user['userid'] != userid:
        return render_template('user/profile.html', user=user)
    else:
        return redirect(url_for('api.add_profile'))

    # redirect to the index, I probably want to address this.
    return redirect(url_for('index'))

@bp.route('/<userid>/exercises', methods=['GET'])
@login_required
def user_exercises(userid):
    
    # get the database
    db = get_db()

    exercises = db.execute(
        'SELECT * FROM user u JOIN exercise e ON u.userid = e.userid WHERE u.userid = ? LIMIT 10',
        (userid,)
    ).fetchall()
    
    if len(exercises) == 0:
        exercises = db.execute(
            'SELECT username FROM user WHERE userid = ?',
            (userid,)
        ).fetchone()
        print(exercises)
        if exercises is None:
            return render_template("errors/404.html"), 404

    return render_template('user/exercise_list.html', exercises=exercises, data={"userid": userid})
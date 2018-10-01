import functools
import uuid

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from exercise_tracker_api.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    userid = str(uuid.uuid4())[:8]

    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        twitter = request.form['twitter']
        facebook = request.form['facebook']
        instagram = request.form['instagram']

        db = get_db()

        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?',
            (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'
        
        if error is None:
    
            dbquery = 'INSERT INTO user (username, password, userid '
            dbparams = [username, generate_password_hash(password), userid]
            values = 'VALUES (?, ?, ?'
            if bio:
                dbquery += ", bio"
                values += ", ?"
                dbparams.append(bio)
            if twitter:
                dbquery += ", twitter"
                values += ", ?"
                dbparams.append(twitter)
            if facebook:
                dbquery += ", facebook"
                values += ", ?"
                dbparams.append(facebook)
            if instagram:
                dbquery += ", instagram"
                values += ", ?"
                dbparams.append(instagram)
            
            dbquery += ")"
            
            values += ")"
            
            dbquery += values

            db.execute(
                dbquery,
                dbparams
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['userid'] = user['userid']
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/delete')
def delete_account():
    userid = g.user['userid']
    db = get_db()
    db.execute(
        'DELETE FROM user WHERE userid=?',
        (userid,)
    )
    db.commit()
    session.clear()
    flash('Account Deleted')
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    userid = session.get('userid')

    if userid is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE userid = ?', (userid,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("You must be logged in to do that.")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
        
    return wrapped_view
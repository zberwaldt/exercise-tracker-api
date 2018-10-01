import os

from flask import Flask, render_template, g, redirect, url_for

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'exercises.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html')

    @app.errorhandler(401)
    def not_authorized(e):
        return render_template('errors/401.html')

    @app.route('/')
    def index():
        if g.user:
            return redirect(url_for('user.user_profile', userid=g.user['user_id']))
        else:
            return redirect(url_for('auth.login'))
            

    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app

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
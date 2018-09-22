import pytest

from exercise_tracker_api.db import get_db
from exercise_tracker_api.api import validate


def test_user_list(client):
    rv = client.get('/user/')

    assert b'Users' in rv.data

def test_user_profile(client):
    rv = client.get('/user/01100000/profile')
    assert b'carl' in rv.data

def test_user_exercises(client,auth):
    rv = auth.login()
    assert rv.data
    rv = client.get('/user/01100000/exercises')
    assert b'carl' in rv.data
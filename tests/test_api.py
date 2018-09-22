import pytest

from exercise_tracker_api.db import get_db
from exercise_tracker_api.api import validate


def test_validate():
    assert validate('2018-08-23') != False

def test_validate_fail():
    assert validate('20180823') == False
    assert validate('2q3524823') == False
    assert validate('20123') == False

def test_new_user(client):
    rv = client.post('/api/exercise/new-user', data={
        "username": "zach",
    })
    print(rv.data)
    assert 'zach' in rv.data

    rv = client.post('/api/exercise/new-user', data={
        'username': None,
    })

    assert 'Please provide a username!' in rv.data

    rv = client.post('/api/exercise/new-user', data= {
        'username': None
    })

    assert "Please provide a username!" in rv.data
        
def test_exercise_add_get(client):
    rv = client.get('/api/exericse/add', follow_redirects=True)
    assert b'Log an excercise' in rv.data

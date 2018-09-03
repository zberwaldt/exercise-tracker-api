from exercise_tracker_api import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/')
    assert b'An exercise logging microservice' in response.data
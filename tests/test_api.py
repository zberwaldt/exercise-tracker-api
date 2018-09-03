from exercise_tracker_api.api import validate

def test_validate():
    assert validate('2018-08-23') != False

def test_validate_fail():
    assert validate('20180823') == False
    assert validate('2q3524823') == False
    assert validate('20123') == False
import pytest
from authentication_module import login, logout

def test_login_success():
    user = {'username': 'testuser', 'password': 'securepass'}
    result = login(user['username'], user['password'])
    assert result['status'] == 'success'
    assert 'token' in result

def test_login_failure():
    user = {'username': 'testuser', 'password': 'wrongpass'}
    result = login(user['username'], user['password'])
    assert result['status'] == 'failure'
    assert 'token' not in result

def test_logout():
    user = {'username': 'testuser', 'password': 'securepass'}
    login_result = login(user['username'], user['password'])
    token = login_result.get('token')
    assert token is not None
    logout_result = logout(token)
    assert logout_result['status'] == 'success'

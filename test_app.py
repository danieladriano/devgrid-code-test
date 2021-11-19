import pytest
from app import app

@pytest.fixture
def test_client():
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture(scope="module")
def get_user():
    with app.test_client() as test_client:
        test_client.post('/weather/1')
        yield test_client

@pytest.fixture(scope="module")
def new_post():
    with app.test_client() as test_client:
        test_client.post('/weather/1')
        yield test_client

def test_get_unauthorized(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/weather/1' endpoint is requested (GET)
    THEN check that the response is unauthorized
    """
    response = test_client.get('/weather/1')
    assert response.status_code == 401
    assert response.json == {"code": 401, "message": "Request not found!"}

def test_post_accepted(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/weather/1' endpoint is requested (POST)
    THEN check that the response is accepted
    """
    response = test_client.post('/weather/1')
    assert response.status_code == 202
    assert response.json == {"code": 202, "message": "Starting weather search!"}

def test_post_request_already_registered(new_post):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/weather/1' endpoint is requested (POST)
    THEN check that the request ID is already registered
    """
    response = new_post.post('/weather/1')
    assert response.status_code == 200
    assert response.json == {"code": 200, "message": "Request already registered!"}

def test_get_request_found(get_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/weather/1' endpoint is requested (GET)
    THEN check that the request ID is found
    """
    response = get_user.get('/weather/1')
    assert response.status_code == 200
    assert response.json == {"code": 200, "request": '1', "progress": '0.00%'}

def test_put_method_not_allowed(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/weather/1' endpoint is requested (PUT)
    THEN check that the response is Method not allowed
    """
    response = test_client.put('/weather/1')
    assert response.status_code == 405

def test_delete_method_not_allowed(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/weather/1' endpoint is requested (PUT)
    THEN check that the response is Method not allowed
    """
    response = test_client.delete('/weather/1')
    assert response.status_code == 405

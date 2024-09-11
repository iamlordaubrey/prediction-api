import pytest

from app import create_app
from config.db_config import db
from seed import seed_models


@pytest.fixture(scope='module')
def test_client():
    app = create_app(test_env=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as testing_client:
        with app.app_context():
            # Create tables
            db.create_all()

            # Seed the database with initial data
            seed_models(test_env=True)

            yield testing_client
            db.drop_all()


@pytest.fixture(scope='module')
def authenticated_client(test_client):
    """Create a test client with authentication."""
    # Register a test user
    test_client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Log in and get the token
    response = test_client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = response.json['token']

    # Set the authorization header with the token
    headers = {
        'Authorization': f'Bearer {token}'
    }

    return test_client, headers


@pytest.fixture(scope='module')
def unauthenticated_client(test_client):
    """Create a test client without authentication."""
    return test_client

def test_register_user(unauthenticated_client):
    """
    Test registering a new user.
    """
    response = unauthenticated_client.post('/auth/register', json={
        'username': 'newuser',
        'password': 'newpassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'


def test_register_user_missing_fields(unauthenticated_client):
    """
    Test user registration with missing fields.
    """
    response = unauthenticated_client.post('/auth/register', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Input payload validation failed'


def test_login_user(authenticated_client):
    """
    Test logging in a user and receiving a JWT token.
    """
    test_client, _ = authenticated_client

    # Attempt to log in
    response = test_client.post('/auth/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200

    assert 'token' in response.json

    # Optionally, validating if the returned tokens are well-formed JWTs
    assert isinstance(response.json['token'], str)


def test_login_user_invalid_credentials(authenticated_client):
    """Test logging in with invalid credentials."""
    test_client, _ = authenticated_client

    # Attempt to log in with incorrect credentials
    response = test_client.post('/auth/login', json={
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert 'error' in response.json
    assert response.json['error'] == 'Invalid username or password'

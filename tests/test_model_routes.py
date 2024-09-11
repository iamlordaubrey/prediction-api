def test_get_models(authenticated_client):
    """
    Test retrieving the list of models.
    """
    test_client, _ = authenticated_client

    response = test_client.get('/models/all')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0


def test_add_model(authenticated_client):
    """
    Test adding a new model for a user.
    """
    test_client, headers = authenticated_client

    # Define the new model data
    new_model_data = {
        'name': 'weighted_sum_model',
        'function_id': 1
    }

    # Send the request to add a new model
    response = test_client.post('/models/add_model', json=new_model_data, headers=headers)
    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'Model added successfully'


def test_get_model(authenticated_client):
    """
    Test retrieving all models for a user.
    """
    test_client, headers = authenticated_client

    # Add a model to retrieve
    test_client.post('/models/add_model', json={
        'name': 'weighted_sum_model',
        'function_id': 1
    }, headers=headers)

    response = test_client.get('/models/user_models', headers=headers)
    assert response.status_code == 200
    assert len(response.json) > 0

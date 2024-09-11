def test_make_prediction(authenticated_client):
    """
    Test making a prediction with a valid model.
    """
    test_client, headers = authenticated_client

    # Add a model to use
    test_client.post('/models/add_model', json={
        'name': 'weighted_sum_model',
        'function_id': 1
    }, headers=headers)

    response = test_client.post('/models/predict', json={
        'model_id': 1,  # ID of the model to use
        'input': {
            'parameters': {'input1': 0.7, 'input2': 0.2},
            'weights': {'input1': 0.5, 'input2': 0.5}
        }  # Example input data for the model
    }, headers=headers)

    assert response.status_code == 200
    assert 'prediction' in response.json  # Ensure the response contains a prediction
    assert isinstance(response.json['prediction'], float)  # Check that prediction is a float

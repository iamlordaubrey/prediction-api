from services.model_logic import weighted_sum_model, weighted_average_model

MODEL_FUNCTIONS = {
    1: weighted_sum_model,
    2: weighted_average_model,
    # Add more models as needed
}


def load_model(function_id):
    """
    Load a model function based on its ID.

    :param function_id: An integer ID representing the model function to load.
    :return: The model function corresponding to the given ID.
    :raises ValueError: If no model function is found for the given ID.
    """
    model_function = MODEL_FUNCTIONS.get(function_id)
    if model_function is None:
        raise ValueError(f"Model function with ID {function_id} not found.")
    return model_function

from sqlalchemy.exc import IntegrityError

from config.db_config import db
from models.prediction import PredictionModel
from models.user import User
from services.model_loader import load_model


def add_model_for_user(user_id, model_name, function_id):
    """
    Adds an existing model to the specified user.

    Checks if the model with the given name and function ID exists in the PredictionModel table.
    If it exists, associates it with the user. If the model is already associated with the user,
    no changes are made.

    :param user_id: The ID of the user to whom the model will be added.
    :param model_name: The name of the model to be added.
    :param function_id: The function ID of the model to be added.
    :return: The PredictionModel instance that was added.
    :raises Exception: If the user is not found, if the model is not found, or if there is an error
    associating the model with the user.
    """
    user = User.query.get(user_id)
    if not user:
        raise Exception("User not found")

    # Check if model exists in the PredictionModel table
    existing_model = PredictionModel.query.filter_by(name=model_name, function_id=function_id).first()

    if not existing_model:
        raise Exception("Model not found")

    # Associate the model with the user if it exists
    if existing_model not in user.prediction_models:
        user.prediction_models.append(existing_model)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception("Error associating model with user")

    return existing_model


def get_model_for_user(model_id, user_id):
    """
    Retrieve a model for the specified user. Raises an exception if the model is not found or does not
    belong to the user.

    Checks if the model with the given ID exists and if it is associated with the specified user.

    :param model_id: The ID of the model to retrieve.
    :param user_id: The ID of the user to whom the model should belong.
    :return: The PredictionModel instance that belongs to the user.
    :raises Exception: If the user is not found, or if the model is not found or does not belong to the user.
    """
    # Fetch the user
    user = User.query.get(user_id)

    if not user:
        raise Exception("User not found")

    # Check if the model exists and belongs to the user using a database query
    model = db.session.query(PredictionModel).join(User.prediction_models).filter(
        User.id == user_id,
        PredictionModel.id == model_id
    ).first()

    if not model:
        raise Exception("Model not found or does not belong to the user")

    return model


def predict_with_model(model, parameters, weights):
    """
    Predict the output using the provided model.

    Loads the model function based on the function ID and uses it to perform the prediction with the
    provided input parameters and weights.

    :param model: The PredictionModel instance to use for prediction.
    :param parameters: Dictionary of input parameters where keys are parameter names and values are
                       their respective values.
    :param weights: Dictionary of weights where keys are parameter names and values are their respective
                    weights.
    :return: The predicted value as a float.
    :raises Exception: If the model function cannot be found for the given function ID.
    """
    # Load the function based on the function_id and run prediction
    model_function = load_model(model.function_id)

    if not model_function:
        raise Exception(f"Model function not found for function_id {model.function_id}")

    # Run prediction with the input data
    return model_function(parameters, weights)

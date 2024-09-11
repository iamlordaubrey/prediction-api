from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError

from services.jwt_handler import token_required
from models.prediction import PredictionModel
from schemas.model_schema import ModelSchema
from services.model_service import add_model_for_user, get_model_for_user, predict_with_model
from utils.api_logger import log_api_call
from utils.error_handler import handle_error

models_namespace = Namespace('models', description='Prediction model related operations')

# Define models
model_schema = models_namespace.model('Model', {
    'name': fields.String(required=True, description='Name of the model', example='weighted_sum_model'),
    'function_id': fields.Integer(required=True, description='ID of the model function', example=1)
})

predict_model = models_namespace.model('Predict', {
    'model_id': fields.Integer(required=True, description='ID of the model', example=1),
    'input': fields.Nested(models_namespace.model('Input', {
        'parameters': fields.Raw(required=True, description='Input parameters for the prediction', example={'input1': 0.7, 'input2': 0.2}),
        'weights': fields.Raw(required=True, description='Weights for the parameters', example={'input1': 0.5, 'input2': 0.5})
    }))
})


@models_namespace.route('/all')
class ListAllModelsResource(Resource):
    def get(self):
        """
        List all prediction models in the application, regardless of user.
        """
        try:
            models = PredictionModel.query.all()
        except Exception as e:
            return handle_error('Error retrieving models: ' + str(e), 500)

        log_api_call(self.id, 'all', request.json)
        return make_response(jsonify([
            {
                'id': model.id,
                'name': model.name,
                'function_id': model.function_id
            } for model in models
        ]), 200)


@models_namespace.route('/user_models')
class ListModelsForUserResource(Resource):
    @token_required
    def get(self, _):
        """
        List all models for the authenticated user.
        """
        try:
            models = PredictionModel.query.filter(PredictionModel.users.any(id=self.id)).all()
        except Exception as e:
            return handle_error(f'Error retrieving models: {str(e)}', 500)

        return make_response(jsonify([
            {
                'id': model.id,
                'name': model.name,
                'function_id': model.function_id
            } for model in models
        ]), 200)


@models_namespace.route('/add_model')
class AddModelResource(Resource):
    @token_required
    @models_namespace.expect(model_schema, validate=True)
    def post(self, _):
        """
        Add a new model for the authenticated user.
        Example JSON:
        {
            "name": "weighted_sum_model",
            "function_id": 1
        }
        """
        data = request.json

        try:
            validated_data = ModelSchema().load(data)
        except ValidationError as e:
            return handle_error('Invalid data: ' + str(e), 400)

        try:
            add_model_for_user(self.id, validated_data['name'], validated_data['function_id'])
        except Exception as e:
            return handle_error('Error adding model: ' + str(e), 500)

        log_api_call(self.id, 'add_model', request.json)
        return make_response(jsonify({'message': 'Model added successfully'}), 201)


@models_namespace.route('/predict')
class PredictResource(Resource):
    @token_required
    @models_namespace.expect(predict_model, validate=True)
    def post(self, _):
        """
        Predict using a user's model.
        Example JSON:
        {
            "model_id": 1,
            "input": {
                "parameters": {"input1": 0.7, "input2": 0.2},
                "weights": {"input1": 0.5, "input2": 0.5}
            }
        }
        """
        data = request.json
        model_id = data.get('model_id')
        input_data = data.get('input')

        if not model_id or not input_data:
            return handle_error('Missing model_id or input data', 400)

        parameters = input_data.get('parameters')
        weights = input_data.get('weights')

        if not parameters or not weights:
            return handle_error('Missing parameters or weights in input data', 400)

        try:
            model = get_model_for_user(model_id, self.id)
        except Exception as e:
            return handle_error('Error getting model: ' + str(e), 404)

        try:
            predicted_value = predict_with_model(model, parameters, weights)
        except Exception as e:
            return handle_error('Prediction failed: ' + str(e), 500)

        log_api_call(self.id, 'predict', request.json)
        return make_response(jsonify({'prediction': predicted_value}), 200)

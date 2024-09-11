from marshmallow import Schema, fields


class ModelSchema(Schema):
    """
    Schema for validating model data.
    """
    name = fields.Str(required=True, example="weighted_sum_model")
    function_id = fields.Int(required=True, example=1)

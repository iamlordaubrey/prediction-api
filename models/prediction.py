from config.db_config import db
from sqlalchemy.orm import relationship

# Association table to handle many-to-many relationship between users and models
user_prediction_models = db.Table(
    'user_prediction_models',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('model_id', db.Integer, db.ForeignKey('prediction_models.id'), primary_key=True)
)


class PredictionModel(db.Model):
    """
    Model for storing prediction models.
    """
    __tablename__ = 'prediction_models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    function_id = db.Column(db.Integer, nullable=False)  # ID to identify the model function

    # Relationship with User model through the association table
    users = relationship('User', secondary=user_prediction_models, back_populates='prediction_models')

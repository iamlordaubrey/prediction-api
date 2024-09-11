from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from config.db_config import db
from models.prediction import user_prediction_models  # Import association table


class User(db.Model):
    """
    User model for storing user credentials.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Many-to-Many relationship with PredictionModel
    prediction_models = relationship(
        'PredictionModel', secondary=user_prediction_models, back_populates='users'
    )

    def set_password(self, password):
        """
        Hash the password and set it for the user.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the hashed password.
        """
        return check_password_hash(self.password, password)

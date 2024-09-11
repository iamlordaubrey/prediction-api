from app import create_app
from config.db_config import db
from models.prediction import PredictionModel


def seed_models(test_env=False):
    app = create_app(test_env)

    with app.app_context():
        # Check if the table is empty
        if db.session.query(PredictionModel).count() == 0:
            # Add initial models
            models = [
                {'name': 'weighted_sum_model', 'function_id': 1},
            ]

            if not test_env:
                models.append({'name': 'weighted_average_model', 'function_id': 2})

            for model in models:
                # Adjust parameters as needed
                new_model = PredictionModel(
                    name=model['name'],
                    function_id=model['function_id'],
                )
                db.session.add(new_model)

            db.session.commit()
            print("Models seeded successfully.")
        else:
            print("Models already seeded.")


if __name__ == "__main__":
    seed_models()

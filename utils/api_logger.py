import logging
from logging.handlers import RotatingFileHandler

# Configure logging with rotation
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def log_api_call(user_id, endpoint, data):
    """
    Log API call details.
    """
    logger.info(f"User {user_id} called {endpoint} with data: {data}")

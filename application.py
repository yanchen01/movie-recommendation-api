import os
import logging

from flask import Flask
from flask_mongoengine import MongoEngine

from models.user import User

application = Flask(__name__)


# Create a custom logger
log_handler = logging.FileHandler('app.log')
log_handler.setLevel(logging.WARNING)
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_format)
logger = logging.getLogger(__name__)
logger.addHandler(log_handler)


# determine local or production db
if application.env == "production":
    # if in production env
    DB_CONNECT_STRING = f"mongodb+srv://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@movie-rec-db.5ica7.mongodb.net/{os.getenv('DB_NAME')}?retryWrites=true&w=majority"
    application.config['MONGODB_SETTINGS'] = {
        "host": DB_CONNECT_STRING
    }
    logger.warning('Cloud Database Connected')
else:
    # if in dev env
    application.config['MONGODB_SETTINGS'] = {
        'db': 'movie-rec',
        'host': 'mongodb://localhost/movie-rec-db'
    }
    logger.warning('Local Database Connected')


db = MongoEngine(application)


@application.route('/')
def index():
    # create a sample user to db
    user = User(
        username="chen",
        name="chen",
        email="ychen@gmail.com",
        password_hash="abc123",
        age=20
    )
    user.save()

    return 'Hellow World!'


# run the app.
if __name__ == "__main__":
    application.run()

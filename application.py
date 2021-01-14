import os
import logging

from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_restplus import Api
from flask_caching import Cache
from flask_jwt_extended import JWTManager


from resources import api_blueprint


from flask_mongoengine import MongoEngine
from models.user import User


import pandas as pd


application = Flask(__name__)
application.register_blueprint(api_blueprint)

CORS(application)


"""
Caching config0
"""
application.config['CACHE_TYPE'] = 'simple'
application.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(application)


@cache.cached(timeout=50, key_prefix='load_recommendations')
def load_recommendations():
    """
    Service functions for recommendation engine
    """
    item_similarity_df = pd.read_csv('./static/item_similarity_df.csv')
    return item_similarity_df


application.item_sim_df = load_recommendations()


"""
Custom logger configuration
"""
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


"""
JWT related configuration. The following functions includes:
1) add claims to each jwt
2) customize the token expired error message 
"""
application.config['JWT_SECRET_KEY'] = os.getenv(
    'JWT_SECRET_KEY')
jwt = JWTManager(application)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead
        return {'is_admin': True}
    return {'is_admin': False}


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
# we have to keep the argument here, since it's passed in by the caller internally
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


@application.route('/')
def index():
    return 'Hellow World!'


# run the app.
if __name__ == "__main__":
    application.run()

from flask import Blueprint
from flask_restplus import Api

from .user import user_ns
from .movie import movie_ns


api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint, title='Movie Recommendation API', doc='/swagger')

""" 
Namespace registering
"""
api.add_namespace(user_ns)
api.add_namespace(movie_ns)

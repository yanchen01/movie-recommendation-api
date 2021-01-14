from flask import current_app as app
from flask_restplus import Resource, reqparse, Namespace
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

import pandas as pd

movie_ns = Namespace('movie', 'Movie methods')

@movie_ns.route('/recommend')
class MovieRecommendation(Resource):
    """
    API Resource for getting movie recommendation
    """

    def get(self):
        recommended_movies = []
        print(app.item_sim_df.head())
        
        
        
        return {
            "message": {
                'recommended_movies': recommended_movies
            }
        }, 200

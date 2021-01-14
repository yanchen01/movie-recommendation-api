from flask import current_app as app, request
from flask_restplus import Resource, reqparse, Namespace, fields
from flask_jwt_extended import (
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)

import pandas as pd

movie_ns = Namespace('movie', 'Movie methods')


def check_seen(recommended_movie, watched_movies):
    for movie_id, movie in watched_movies.items():
        if recommended_movie == movie["title"]:
            return True
    return False


def get_similar_movies(movie_name, user_rating):
    try:
        similar_score = app.item_sim_df[movie_name]*(user_rating-2.5)
        similar_movies = similar_score.sort_values(ascending=False)
    except:
        print("don't have movie in model")
        similar_movies = pd.Series([])

    return similar_movies


movie_recommend_resource_fields = {
    'watched_movies': fields.List
}

_watched_movie_parser = reqparse.RequestParser()
_watched_movie_parser.add_argument(
    'watched_movies',
    type=str,
    required=False,  # True
    location=['form', 'json'],
    help='This field cannot be empty.'
)


@movie_ns.route('/recommend')
class MovieRecommendation(Resource):
    """
    API Resource for getting movie recommendation
    """

    @movie_ns.doc(
        responses={
            200: "Recommended movies successfully.",
            400: "Recommended movies unsuccessfully.",
        },
        params={
            'watched_movies': {'in': 'formData', 'required': True}
        }
    )
    def post(self):
        watched_movies = request.get_json()

        similar_movies = pd.DataFrame()
        for movie_id, movie in watched_movies.items():
            similar_movies = similar_movies.append(get_similar_movies(
                movie["title"], movie["rating"]), ignore_index=True)

        recommended_movies = []
        all_recommend = similar_movies.sum().sort_values(ascending=False)

        for movie, score in all_recommend.iteritems():
            if not check_seen(movie, watched_movies):
                recommended_movies.append(movie)

        if len(recommended_movies) > 100:
            recommended_movies = recommended_movies[0:100]

        return {
            "message": {
                'recommended_movies': recommended_movies
            }
        }, 200

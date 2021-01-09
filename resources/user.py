from flask_restful import Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_required
)
from models.user import User


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('name',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

bcrypt = Bcrypt()


class UserRegister(Resource):
    """
    API Resource for registering a user
    """

    def post(self):
        data = _user_parser.parse_args()

        # check if current user already exist
        if User.objects(email=data['email']).count() != 0:
            return {"message": "A user with that email already exists"}, 400

        # create new user
        pw_hash = bcrypt.generate_password_hash(data['password'])
        new_user = User(
            username=data['email'],
            email=data['email'],
            password_hash=pw_hash,
            name=data['name']
        )

        new_user.save()
        return {"message": "User created successfully."}, 400

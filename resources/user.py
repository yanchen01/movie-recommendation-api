from flask_restplus import Resource, reqparse, Namespace
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


user_ns = Namespace('user', 'User methods')


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


@user_ns.route('/register')
class UserRegister(Resource):
    """
    API Resource for registering a user
    """
    @user_ns.doc(
        responses={
            200: "Signup successful",
            400: "There's already an account with the provided email.",
            403: "Signup unsuccessful. Please try again."
        },
        params={
            'email': {'in': 'json', 'required': True},
            'password': {'in': 'json', 'required': True},
            'name': {'in': 'json', 'required': True},
        }
    )
    def post(self):
        data = _user_parser.parse_args()

        try:
            # check if current user already exist
            User.objects(email=data['email'])
            return {"message": "A user with that email already exists"}, 400
        except:
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

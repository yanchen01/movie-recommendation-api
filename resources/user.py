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
from models.user import User as UserModel


user_ns = Namespace('user', 'User methods')


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
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
            'username': {'in': 'json', 'required': True},
            'email': {'in': 'json', 'required': True},
            'password': {'in': 'json', 'required': True},
            'name': {'in': 'json', 'required': True},
        }
    )
    def post(self):
        data = _user_parser.parse_args()

        # check if current user already exist
        user = UserModel.objects(email=data['email'])

        if user:
            return {"message": "A user with that email already exists"}, 400

        # create new user
        pw_hash = bcrypt.generate_password_hash(data['password'])
        new_user = UserModel(
            username=data['username'],
            email=data['email'],
            password_hash=pw_hash,
            name=data['name']
        )

        try:
            new_user.save()
            return {"message": "User created successfully."}, 200
        except:
            return {"message": "Signup unsuccessful. Please try again."}, 403


@user_ns.route('/login')
class UserLogin(Resource):
    """
    API Resource for registering a user
    """
    @user_ns.doc(
        responses={
            200: "Log in successful",
            401: "Invalid credentials",
            403: "Log in unsuccessful. Please try again."
        },
        params={
            'username': {'in': 'json', 'required': True},
            'email': {'in': 'json', 'required': True},
            'password': {'in': 'json', 'required': True},
            'name': {'in': 'json', 'required': True},
        }
    )
    def post(self):
        data = _user_parser.parse_args()
        try:
            user = UserModel.objects(email=data['email']).get()
            if bcrypt.check_password_hash(user.password_hash, data['password']):
                access_token = create_access_token(
                    identity=user.username, fresh=True)
                refresh_token = create_refresh_token(user.username)

                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200

            return {"message": "Invalid Credentials!"}, 401
        except:
            return {"message": "Log in unsuccessful. Please try again."}, 403


@user_ns.route('/logout')
class UserLogOut(Resource):
    """
    API Resource for logging out a user
    """
    @user_ns.doc(
        responses={
            200: "Logged out successful",
        }
    )
    @jwt_required
    def post(self):
        return {"messsage": "Successfully logged out"}, 200


_user_update_parser = reqparse.RequestParser()
_user_update_parser.add_argument('username',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
_user_update_parser.add_argument('email',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )
_user_update_parser.add_argument('name',
                                 type=str,
                                 required=True,
                                 help="This field cannot be blank."
                                 )


@user_ns.route('/info/<username>')
class User(Resource):
    """
    API Resource for user model CRUD operations
    """
    @user_ns.doc(
        responses={
            200: "Successful",
            404: "User not found",
            405: "Unsuccessful update."
        },
        params={
            'username': {'in': 'json', 'required': True},
            'email': {'in': 'json', 'required': True},
            'name': {'in': 'json', 'required': True},
        }
    )
    @jwt_required
    def get(self, username):
        user = UserModel.objects(username=username).get()

        if not user:
            return {'message': 'User Not Found'}, 404

        return user.json(), 200

    @jwt_required
    def put(self, username):
        fields = _user_update_parser.parse_args()
        try:
            user = UserModel.objects(username=username).get()
            user.update(**fields)
            return {
                'message': 'Successfully updated!',
            }, 200
        except:
            return {'message': 'Unsuccessful update.'}, 405

    @jwt_required
    def delete(self, username):
        user = UserModel.objects(username=username).get()

        if not user:
            return {'message': 'User Not Found'}, 404

        # delete user if exists
        user.delete()
        return {'message': 'User deleted.'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200

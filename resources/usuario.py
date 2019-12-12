from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

attributes = reqparse.RequestParser()
attributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be left in blank!")
attributes.add_argument('password', type=str, required=True, help="The field 'password' cannot be left in blank!")

class User(Resource):
    
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found'}, 404 # not found
    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'Internal Server Error ocurred trying to delete user'}, 500
            return {'message': 'User deleted!'}
        return {'message': 'User not found'}

class UserRegister(Resource):
    # CREATING A USER
    @jwt_required
    def post(self):
    
        data = attributes.parse_args()

        if UserModel.find_by_login(data['login']):
            return {"message": "The login '{}' already exists".format(data['login'])}
        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created succesfully!'}, 201 # CREATED

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = attributes.parse_args()

        user = UserModel.find_by_login(data['login'])

        if user and safe_str_cmp(user.password, data['password']):
            token_access = create_access_token(identity=user.user_id)
            return {'access_token': token_access}, 200
        return {'message': 'The username or password is incorrect.'}, 401

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Loggedout successfully'}, 200
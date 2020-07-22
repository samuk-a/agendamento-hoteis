from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from models.usuario import UserModel
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")

# /usuarios/{user_id}
class User(Resource):
    def get(self, user_id):
        user = UserModel.find(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find(user_id)
        if user:
            try:
                user.delete()
            except:
                return {'message':'An internal error occurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}, 200
        return {'message': 'User not found.'}, 404

# /cadastro
class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}

        user = UserModel(**dados)
        user.save()
        return {"message": "User created successfully!"}, 201

# /login
class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token = create_access_token(identity=user.id)
            return {'access_token':token}, 200
        return {'message':'The username or password do not match.'}, 401

# /logout
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully'}, 200

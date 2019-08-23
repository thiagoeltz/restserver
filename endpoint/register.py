import datetime
from flask_restful import Resource, reqparse
from endpoint.hash_generator import HashGenerator
from flask_jwt_extended import (create_access_token, create_refresh_token)
from model.redis_connection import RedisConnection

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        user = data['username']
        valid_user = self.validation(user)
        if valid_user is True:
            return self.create_user(data)
        else:
            return valid_user

    def create_user(self, data):
        try:
            access_token = self.create_user_access_token(data['username'])
            refresh_token = self.create_user_refresh_token(data['username'])
            RedisConnection().list_add(data['username'], (HashGenerator.generate_hash(data['password'])))
            RedisConnection().list_add(data['username'], access_token)
            RedisConnection().list_add(data['username'], refresh_token)
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            return {'message': 'Something went wrong' + str(e)}, 500

    def create_user_refresh_token(self, username):
        refresh = datetime.timedelta(days=60)
        refresh_token = create_refresh_token(identity=username, expires_delta=refresh)
        return refresh_token

    def create_user_access_token(self, username):
        expires = datetime.timedelta(days=3)
        access_token = create_access_token(identity=username, expires_delta=expires)
        return access_token

    def validation(self, user):
        if RedisConnection().list_verify(user) is True:
            return {'message': 'User {} already exists'.format(user)}
        if "@" not in str(user) or "." not in str(user):
            return {'message': 'Use a valid e-mail as User'}
        else:
            return True

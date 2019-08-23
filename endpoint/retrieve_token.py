from flask_restful import Resource, reqparse
from endpoint.hash_generator import HashGenerator
from model.redis_connection import RedisConnection


parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRetrieveToken(Resource):

    def post(self):
        get_username = 0
        get_token = 1
        get_refresh = 2
        data = parser.parse_args()
        user = data['username']
        if RedisConnection().list_verify(user) is False:
            return {'message': 'User {} not exists'.format(data['username'])}
        password = RedisConnection().list_get(user, get_username, get_username)
        if HashGenerator.verify_hash(data['password'], password[0]) is False:
            return {'message': 'Wrong credentials'}

        return {

            'message': 'Bellow is your tokens',
            'access_token': RedisConnection().list_get(user, get_token, get_token),
            'refresh_token': RedisConnection().list_get(user, get_refresh, get_refresh)

        }

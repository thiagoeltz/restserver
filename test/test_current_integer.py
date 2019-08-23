from mock import patch
import json

import unittest

from wsgi import application

app = application.test_client()


class TestRegister(unittest.TestCase):

    @patch('model.redis_connection.RedisConnection.init_connection')
    def test_current_integer_expired_token(self, mock_init_connection):
        response = app.get('/current',
                            headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1'
                                                      'NTExMTU0MTEsIm5iZiI6MTU1MTExNTQxMSwianRpIjoiNGQ0NzA0YzYtY'
                                                      '2QzZi00MjkxLWIyODEtZjU0NDA5ZDMwNDZjIiwiZXhwIjoxNTU2Mjk5ND'
                                                      'ExLCJpZGVudGl0eSI6InRlc3RAZ21haWwuY29tIiwidHlwZSI6InJlZn'
                                                      'Jlc2gifQ.Id0sgTu5tqKETVybiyKhi-Sw9_zZ7MC-uXCQIJXX_48'},
                            content_type='application/json')

        self.assertEqual(response.status_code, 422)

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_add')
    @patch('endpoint.register.UserRegistration.create_user_refresh_token')
    @patch('model.redis_connection.RedisConnection.get_value_redis_db')
    @patch('model.redis_connection.RedisConnection.insert_redis_db')
    @patch('model.redis_connection.RedisConnection.exist_value_redis_db')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_current_integer_without_value(self, mock_list_verify, mock_exist_value, mock_insert_redis_db,
                                        mock_get_value_redis_db, mock_refresh_token, mock_list_add,
                                        mock_init_connection):
        mock_list_verify.side_effect = lambda name: name != "test@gmail.com"
        mock_get_value_redis_db.side_effect = lambda key: 0
        mock_exist_value.side_effect = lambda identity: False
        mock_refresh_token.side_effect = lambda identity: "refresh_token"

        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')
        token = json.loads(response.get_data(as_text=True))["access_token"]
        response = app.get('/current',
                           headers={'Authorization': 'Bearer ' + token + ''},
                           content_type='application/json')
        self.assertEqual(response.get_data(as_text=True), '{\n    "Integer": [\n        {\n            "current": 0\n        }\n    ]\n}\n')

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_add')
    @patch('endpoint.register.UserRegistration.create_user_refresh_token')
    @patch('model.redis_connection.RedisConnection.get_value_redis_db')
    @patch('model.redis_connection.RedisConnection.insert_redis_db')
    @patch('model.redis_connection.RedisConnection.exist_value_redis_db')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_current_integer_generation_with_value(self, mock_list_verify, mock_exist_value, mock_insert_redis_db,
                                                   mock_get_value_redis_db, mock_refresh_token, mock_list_add,
                                                   mock_init_connection):
        mock_list_verify.side_effect = lambda name: name != "test@gmail.com"
        mock_get_value_redis_db.side_effect = lambda key: 1
        mock_exist_value.side_effect = lambda identity: True
        mock_refresh_token.side_effect = lambda identity: "refresh_token"

        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')
        token = json.loads(response.get_data(as_text=True))["access_token"]
        response = app.get('/current',
                           headers={'Authorization': 'Bearer ' + token + ''},
                           content_type='application/json')
        self.assertEqual(response.get_data(as_text=True), '{\n    "Integer": [\n        {\n            "current": 1\n        }\n    ]\n}\n')

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('endpoint.register.UserRegistration.create_user_refresh_token')
    @patch('model.redis_connection.RedisConnection.get_value_redis_db')
    @patch('model.redis_connection.RedisConnection.insert_redis_db')
    @patch('endpoint.current_integer.IntegerVerifyCurrent.get_current_value')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_current_with_set_integer(self, mock_list_verify, mock_get_current_value,  mock_insert_redis_db,
                                                   mock_get_value_redis_db, mock_refresh_token,
                                                   mock_init_connection):
        mock_list_verify.side_effect = lambda name: name != "test@gmail.com"
        mock_get_value_redis_db.side_effect = lambda key: 1155
        mock_get_current_value.side_effect = lambda: 1155
        mock_refresh_token.side_effect = lambda identity: "refresh_token"

        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')
        token = json.loads(response.get_data(as_text=True))["access_token"]
        response = app.put('/current',
                           headers={'Authorization': 'Bearer ' + token + ''},
                           data={'current': 1155},
                           content_type='application/json')
        self.assertEqual(response.get_data(as_text=True), '{\n    "Integer": [\n        {\n            "current": 1155\n        }\n    ]\n}\n')

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('endpoint.register.UserRegistration.create_user_refresh_token')
    @patch('model.redis_connection.RedisConnection.get_value_redis_db')
    @patch('model.redis_connection.RedisConnection.insert_redis_db')
    @patch('endpoint.current_integer.IntegerVerifyCurrent.get_current_value')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_current_with_negative_integer(self, mock_list_verify, mock_get_current_value, mock_insert_redis_db,
                                      mock_get_value_redis_db, mock_refresh_token,
                                      mock_init_connection):
        mock_list_verify.side_effect = lambda name: name != "test@gmail.com"
        mock_get_value_redis_db.side_effect = lambda key: True
        mock_get_current_value.side_effect = lambda: int(-1)
        mock_refresh_token.side_effect = lambda identity: "refresh_token"

        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')
        token = json.loads(response.get_data(as_text=True))["access_token"]
        response = app.put('/current',
                           headers={'Authorization': 'Bearer ' + token + ''},
                           data={'current': 1155},
                           content_type='application/json')
        self.assertEqual(response.get_data(as_text=True), '{\n    "Integer": [\n        {\n            "current": "Insert a valid number, >=0"\n        }\n    ]\n}\n')


if __name__ == '__main__':
    unittest.main()


from mock import patch
import unittest

from wsgi import application

app = application.test_client()


class TestUserRetrieveToken(unittest.TestCase):

    @patch('model.redis_connection.RedisConnection.init_connection')
    def test_invalid_input(self, mock_init_connection):
        response = app.post('/retrieve',
                            data='{"username": "test@gmail.com"}',
                            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_user_not_exists(self, mock_list_verify, mock_init_connection):
        mock_list_verify.side_effect = lambda name: name != "test@gmail.com"

        response = app.post('/retrieve',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')

        self.assertEqual(response.get_data(as_text=True), '{\n    "message": "User test@gmail.com not exists"\n}\n')

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_verify')
    @patch('model.redis_connection.RedisConnection.list_get')
    @patch('endpoint.hash_generator.HashGenerator.verify_hash')
    def test_invalid_user_pass(self, mock_verify_hash, mock_list_get, mock_list_verify, mock_init_connection ):
        mock_list_verify.side_effect = lambda name: True
        mock_verify_hash.side_effect = lambda password, valid_hash: False
        response = app.post('/retrieve',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')

        self.assertEqual(response.get_data(as_text=True), '{\n    "message": "Wrong credentials"\n}\n')


if __name__ == '__main__':
    unittest.main()


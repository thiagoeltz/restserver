from mock import patch
import unittest

from wsgi import application

app = application.test_client()


def throw_exception(name):
    raise Exception('error')


class TestRegister(unittest.TestCase):

    @patch('model.redis_connection.RedisConnection.init_connection')
    def test_invalid_input(self, mock_init_connection):
        response = app.post('/registration',
                            data='{"username": "test@gmail.com"}',
                            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_add')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_status_ok(self, mock_list_verify, mock_list_add, mock_init_connection):
        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')

        self.assertEqual(response.status_code, 200)

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_verify')
    @patch('endpoint.register.UserRegistration.create_user_access_token')
    def test_unexpected_exception_status(self, mock_access_token, mock_list_verify, mock_init_connection):
        mock_list_verify.side_effect = lambda name: False
        mock_access_token.side_effect = throw_exception
        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')

        self.assertEqual(response.status_code, 500)

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_add')
    @patch('endpoint.register.UserRegistration.create_user_refresh_token')
    @patch('endpoint.register.UserRegistration.create_user_access_token')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_token_generation(self, mock_list_verify, mock_access_token, mock_refresh_token, mock_list_add, mock_init_connection):
        mock_list_verify.side_effect = lambda name: name != "test@gmail.com"
        mock_access_token.side_effect = lambda identity: "access_token"
        mock_refresh_token.side_effect = lambda identity: "refresh_token"

        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')

        self.assertEqual(response.get_data(as_text=True), '{\n    "message": "User test@gmail.com was created",\n    "access_token": "access_token",\n    "refresh_token": "refresh_token"\n}\n')

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_user_already_exists(self, mock_list_verify, mock_init_connection):
        mock_list_verify.side_effect = lambda name: name == "test@gmail.com"

        response = app.post('/registration',
                            data='{"username": "test@gmail.com","password": "bla"}',
                            content_type='application/json')

        self.assertEqual(response.get_data(as_text=True), '{\n    "message": "User test@gmail.com already exists"\n}\n')

    @patch('model.redis_connection.RedisConnection.init_connection')
    @patch('model.redis_connection.RedisConnection.list_verify')
    def test_user_valid_email(self, mock_list_verify, mock_init_connection):
        mock_list_verify.side_effect = lambda name: name != "test"

        response = app.post('/registration',
                            data='{"username": "test","password": "bla"}',
                            content_type='application/json')

        self.assertEqual(response.get_data(as_text=True), '{\n    "message": "Use a valid e-mail as User"\n}\n')


if __name__ == '__main__':
    unittest.main()


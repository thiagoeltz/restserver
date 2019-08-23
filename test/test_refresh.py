from mock import patch
import unittest

from wsgi import application

app = application.test_client()


class TestRegister(unittest.TestCase):

    @patch('model.redis_connection.RedisConnection.init_connection')
    def test_refresh_invalid_authorization(self, mock_init_connection):
        response = app.post('/refresh',
                            headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTExMTU0MTEsIm5iZiI6MTU1MTExNTQxMSwianRpIjoiNGQ0NzA0YzYtY2QzZi00MjkxLWIyODEtZjU0NDA5ZDMwNDZjIiwiZXhwIjoxNTU2Mjk5NDExLCJpZGVudGl0eSI6InRlc3RAZ21haWwuY29tIiwidHlwZSI6InJlZnJlc2gifQ.Id0sgTu5tqKETVybiyKhi-Sw9_zZ7MC-uXCQIJXX_48'},
                            content_type='application/json')

        self.assertEqual(response.status_code, 422)

    @patch('model.redis_connection.RedisConnection.init_connection')
    def test_missing_authorization(self, mock_init_connection):
        response = app.post('/refresh',
                            data='{"username": "test@gmail.com"}',
                            content_type='application/json')

        self.assertEqual(response.status_code, 401)

    @patch('model.redis_connection.RedisConnection.init_connection')
    def test_refresh_authorization_given_a_token(self, mock_init_connection):
        response = app.post('/refresh',
                            headers={'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTExMTU0'
                                                      'MTEsIm5iZiI6MTU1MTExNTQxMSwianRpIjoiNGQ0NzA0YzYtY2QzZi00MjkxL'
                                                      'WIyODEtZjU0NDA5ZDMwNDZjIiwiZXhwIjoxNTU2Mjk5NDExLCJpZGVudGl0eSI6'
                                                      'InRlc3RAZ21haWwuY29tIiwidHlwZSI6InJlZnJlc2gifQ.Id0sgTu5tqKETVybi'
                                                      'yKhi-Sw9_zZ7MC-uXCQIJXX_48'},
                            content_type='application/json')
        result = response.get_data(as_text=True)
        self.assertEqual(response.get_data(as_text=True), result)


if __name__ == '__main__':
    unittest.main()


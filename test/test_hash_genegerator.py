import unittest
from endpoint.hash_generator import HashGenerator


class TestRedis(unittest.TestCase):

    def test_generate_hash(self):
        value = HashGenerator.generate_hash("test")
        assert str(value).__len__() > 80

    def test_verify_hash(self):
        value = HashGenerator.generate_hash("test")
        result = HashGenerator.verify_hash("test", value)
        assert result is True


if __name__ == '__main__':
    unittest.main()
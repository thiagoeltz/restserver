import unittest
from model.redis_connection import RedisConnection


class TestRedis(unittest.TestCase):

    def test_insert_redis_db(self):
        db = RedisConnection()
        db.insert_redis_db("foo", "bar")
        assert "bar" in db.get_value_redis_db("foo") == "bar"

    def test_exist_value_redis_db(self):
        db = RedisConnection()
        value = db.exist_value_redis_db("foo")
        assert value is True

    def test_list_add(self):
        db = RedisConnection()
        db.list_add("bar", "1")
        value = db.list_get("bar", 0, 0)
        assert value[0] is "1"
        assert db.list_verify("bar") is True
        db.list_del("bar")


if __name__ == '__main__':
    unittest.main()

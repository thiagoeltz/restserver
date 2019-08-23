import platform
import redis


class RedisConnection:

    def __init__(self):
        self.__connect = self.init_connection()

    def init_connection(self):
        if platform.system() == "Linux":
            return redis.Redis(
                host='10.131.54.16',
                port=6379,
                password='Mzg5MWZiNzgwYmU1NDZkOGUyMWUzNjk2ZGEyYmFhOTE6NzZlMTgyMmZiOTQ4OTQ2NTczZjhlNTI0ZDA3ODkwN3o=',
                charset="utf-8",
                decode_responses=True)
        elif platform.system() == "Windows":
            return redis.Redis(
                host='127.0.0.1',
                port=6379,
                charset="utf-8",
                decode_responses=True)

    @property
    def connect(self):
        return self.__connect

    def insert_redis_db(self, key, value):
        result = self.connect.set(key, value)
        return result

    def get_value_redis_db(self, key):
        result = self.connect.get(key)
        return result

    def delete_value_redis_db(self, key):
        result = self.connect.delete(key)
        return result

    def exist_value_redis_db(self, key):
        result = self.connect.exists(key)
        if result > 0:
            return True
        return False

    def list_add(self, name, values):
        result = self.connect.rpush(name, values)
        return result

    def list_get(self,name, start_range, end_range):
        result = self.connect.lrange(name, start_range, end_range)
        return result

    def list_del(self, list_name):
        result = self.connect.delete(list_name)
        return result

    def list_pop(self, list_name):
        result = self.connect.lpop(list_name)
        return result

    def list_add_left(self, name, values):
        result = self.connect.lpush(name, values)
        print(result)

    def list_verify(self, name):
        result = self.connect.lindex(name, 0)
        if result is "" or result is None:
            return False
        return True



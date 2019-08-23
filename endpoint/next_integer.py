from flask_restful import Resource
from flask_jwt_extended import jwt_required
from model.redis_connection import RedisConnection


class IntegerVerifyNext(Resource):

    @jwt_required
    def get(self):
        db = RedisConnection()
        if db.exist_value_redis_db("Integer") is False:
            db.insert_redis_db("Integer", 0)
            integer = {"Integer": [{"next": db.get_value_redis_db("Integer")}]}
            return integer
        else:
            value = int(db.get_value_redis_db("Integer")) + 1
            db.insert_redis_db("Integer", value)
            integer = {"Integer": [{"next": db.get_value_redis_db("Integer")}]}
            return integer

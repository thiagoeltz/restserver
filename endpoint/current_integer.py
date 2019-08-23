from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from model.redis_connection import RedisConnection


class IntegerVerifyCurrent(Resource):

    @jwt_required
    def get(self):
        db = RedisConnection()
        if db.exist_value_redis_db("Integer") is False:
            db.insert_redis_db("Integer", 0)
            integer = {"Integer": [{"current": db.get_value_redis_db("Integer")}]}
            return integer
        else:
            integer = {"Integer": [{"current": db.get_value_redis_db("Integer")}]}
            return integer

    @jwt_required
    def put(self):
        db = RedisConnection()
        value = self.get_current_value()
        if int(value) >= 0:
            db.insert_redis_db("Integer", value)
            integer = {"Integer": [{"current": db.get_value_redis_db("Integer")}]}
            return integer
        else:
            integer = {"Integer": [{"current": "Insert a valid number, >=0"}]}
            return integer

    def get_current_value(self):
        value = request.json.get('current', None)
        return value

from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
from flask_cors import CORS

from database import PostSQL as General_Methods
from items import items_

app = Flask(__name__)
api = Api(app)
CORS(app)


class Status(Resource):
    @staticmethod
    def get() -> Response:
        return jsonify({"success": True, "response": "API is up!"})


class Top(Resource):
    def get(self, limit=10) -> Response:
        if limit > 100: limit = 100
        return jsonify(General_Methods().get_top_balance(limit))


class BalanceSum(Resource):
    def get(self) -> Response:
        return jsonify(General_Methods().get_sum_balance())

class Items(Resource):
    def get(self) -> Response:
        return jsonify(items_)


class User(Resource):
    def get(self, user_id) -> Response:
        data = General_Methods(user_id).check_user(); data["username"] = "hidden"
        return jsonify(data)


api.add_resource(Status, '/')
api.add_resource(Top, '/top', '/top/<int:limit>')
api.add_resource(BalanceSum, '/sum')
api.add_resource(Items, '/items')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == "__main__":
    app.run()

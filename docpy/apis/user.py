import json

from sys import exc_info
from core.utils import serialize
from core.manager import UserManager
from flask_restplus import Namespace, Resource, fields


api = Namespace('user', description='Manage Users')

user_m = api.model(
    'User Model',
    {'username': fields.String(required=True)}
)

manager = UserManager()


@api.route("/")
class User(Resource):

    @api.expect(user_m, validate=True)
    def post(self):
        data = api.payload
        try:
            user_id = manager.create_User(data)
            data.update({'id': user_id})
            return data
        except Exception as e:
            err = exc_info()[1]
            api.abort(400, status="400", error=str(err))


@api.route("/<int:id>")
class UserRecord(Resource):

    # TODO: Security risk
    def get(self, id):
        data = api.payload
        try:
            user = manager.get_User_by_ID(id)
            resp = json.dumps(user, default=serialize)
            return json.loads(resp)
        except Exception as e:
            err = exc_info()[1]
            api.abort(400, status="400", error=str(err))

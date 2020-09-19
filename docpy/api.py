import json
from os import urandom
from docpy import __version__ as version

# exception raise from flask_restplus
try:
    import werkzeug
    werkzeug.cached_property
except AttributeError:
    werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, session as fsession
from sys import exc_info
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from manager import UserManager, AppointmentManager
from utils import serialize


# -------------------------
# API DESCRIPTION
app = Flask(__name__)
app.secret_key = urandom(24)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app, version=version,
    title="DocPy APIs",
    description="API for Doctor's Appointment",
)

# TODO: register /api/ blueprint

# -------------------------
# NAMESPACES
user_ns = api.namespace('user', description='Manage Users')
appt_ns = api.namespace('appointments', description='Manage Appointments')


# -------------------------
# MODELS
user_m = api.model(
    'User Model',
    {'username': fields.String(required=True)}
)

appt_m = api.model(
    'Apppointment Model', {
        'patient_name': fields.String(required=True),
        'date': fields.Date(required=True),
        'from_time': fields.String(required=True),
        'to_time': fields.String(required=True),
        'comment': fields.String(required=True),
        'user_id': fields.Integer(required=True)
    }
)

# -------------------------
# Manager Mixin

class UserMixin:
    manager = UserManager()


class AppointmentMixin:
    manager = AppointmentManager()


# -------------------------
# API PROPER
# A. USER

@user_ns.route("/")
class User(Resource, UserMixin):

    @api.expect(user_m, validate=True)
    def post(self):
        data = user_ns.payload
        try:
            user_id = self.manager.create_User(data)
            data.update({'id': user_id})
            return data
        except Exception as e:
            err = exc_info()[1]
            user_ns.abort(400, status="400", error=str(err))


@user_ns.route("/<int:id>")
class UserRecord(Resource, UserMixin):

    # TODO: Security risk
    def get(self, id):
        data = user_ns.payload
        try:
            user = self.manager.get_User_by_ID(id)
            resp = json.dumps(user, default=serialize)
            return json.loads(resp)
        except Exception as e:
            err = exc_info()[1]
            user_ns.abort(400, status="400", error=str(err))


# A. APPOINTMENT

@appt_ns.route("/")
class Appointment(Resource, AppointmentMixin):

    @api.expect(appt_m, validate=True)
    def post(self):
        data = appt_ns.payload
        try:
            appt_id = self.manager.create_Appointment(data)
            data.update({'id': appt_id})
            return data
        except Exception as e:
            err = exc_info()[1]
            user_ns.abort(400, status="400", error=str(err))

    def get(self):
        data = appt_ns.payload
        try:
            # TODO Parsing Here
            return {
                "status": "GET Appointment by RANGE"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")



@appt_ns.route("/<int:id>")
class AppointmentRecord(Resource, AppointmentMixin):

    def update(self, id):
        data = appt_ns.payload
        try:
            appt_id = self.manager.create_Appointment(data)
            data.update({'id': appt_id})
            return {'satus': 'True'}
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")

    def delete(self, id):
        try:
            return {
                "status": "DELTE APPOINTMENT BY ID"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")


# UTILITY endpoints
# @app.route('/login/<string:username>', methods=['GET'])
# def login(username):
#     manager = UserManager()
#     r = manager.get_User(username)
#     print(r)
#     fsession['CURRENT_USER_ID'] = username
#     return {"status": "Login Success"}

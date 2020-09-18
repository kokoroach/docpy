# exception raise from flask_restplus
try:
    import werkzeug
    werkzeug.cached_property
except AttributeError:
    werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix


# -------------------------
# API DESCRIPTION
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app, version="1.0",
    title="DocPY APIs",
    description="API for Doctor's Appointment",
)


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
# API PROPER


# A. USER

@user_ns.route("/")
class User(Resource):

    @api.expect(user_m, validate=True)
    def post(self):
        try:
            return {
                "status": "New User added"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")


@user_ns.route("/<int:id>")
class UserRecord(Resource):

    def get(self, id):
        try:
            return {
                "A": f"Get User: {id}"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")


# A. APPOINTMENT

@appt_ns.route("/")
class Appointment(Resource):

    @api.expect(appt_m, validate=True)
    def post(self):
        try:
            return {
                "status": "New Appointment added"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")

    def get(self):
        try:
            # TODO Parsing Here
            return {
                "status": "GET Appointment by RANGE"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")



@appt_ns.route("/<int:id>")
class AppointmentRecord(Resource):

    def update(self, id):
        try:
            return {
                "status": "GET APPOINTMENT BY ID"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")

    def delete(self, id):
        try:
            return {
                "status": "DELTE APPOINTMENT BY ID"
            }
        except Exception as e:
            user_ns.abort(400, e.__doc__, statusCode="400")


if __name__ == '__main__':
    app.run(debug=True)

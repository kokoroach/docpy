import json

from sys import exc_info
from core.utils import serialize
from core.manager import AppointmentManager
from flask_restplus import Namespace, Resource, fields


api = Namespace('appointments', description='Manage Appointments')

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
user_id_m = api.model(
    'UserID Model', {
        'user_id': fields.Integer(required=True)
    }
)

manager = AppointmentManager()


@api.route("/")
class Appointment(Resource):

    @api.expect(appt_m, validate=True)
    def post(self):
        data = api.payload
        try:
            appt_id = manager.create_Appointment(data)
            data.update({'id': appt_id})
            return data
        except Exception:
            err = exc_info()[1]
            api.abort(400, status="400", error=str(err))

    # TODO Simplify
    @api.param('from', description='From Date', required=True)
    @api.param('to', description='To Date', required=True)
    @api.doc(params={"id": "An ID", "description": "My resource"})
    def get(self):
        data = api.payload
        print(data)
        try:
            # TODO Parsing Here
            # TODO Mask response. only date and time range
            return {
                "status": "GET Appointment by RANGE"
            }
        except Exception:
            err = exc_info()[1]
            user_ns.abort(400, status="400", error=str(err))


@api.route("/<int:id>")
class AppointmentRecord(Resource):

    @api.expect(appt_m)
    def patch(self, id):
        data = api.payload
        try:
            appt_info = manager.update_Appointment(id, data)
            resp = json.dumps(appt_info, default=serialize)
            return json.loads(resp)
        except Exception:
            err = exc_info()[1]
            api.abort(400, status="400", error=str(err))

    @api.expect(user_id_m)
    def delete(self, id):
        data = api.payload
        try:
            user_id = data.get('user_id')
            status = manager.delete_Appointment(id, user_id)
            if status:
                return {'status': 'success'}
        except Exception:
            err = exc_info()[1]
            api.abort(400, status="400", error=str(err))

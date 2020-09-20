import json

from sys import exc_info
from core.utils import serialize
from core.manager import AppointmentManager
from flask_restplus import Namespace, Resource, fields, reqparse


api = Namespace('appointment', description='Manage Appointments')

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

    get_params = {
        'from': {'description': 'Date in HH:MM:SS', 'required': 'True'},
        'to': {'description': 'Date in HH:MM:SS', 'required': 'True'}
    }
    @api.doc(params=get_params)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('from', type=str, required=True)
            parser.add_argument('to', type=str, required=True)
            args = parser.parse_args()

            appts = manager.get_Appointments_by_Range(args['from'], args['to'])
            resp = json.dumps(appts, default=serialize)
            resp = json.loads(resp)
            return {"appointments": resp}
        except Exception:
            err = exc_info()[1]
            api.abort(400, status="400", error=str(err))


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

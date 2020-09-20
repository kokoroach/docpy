from sqlalchemy import and_
from core.db_model import User, Appointment


class Registrar:

    def __init__(self, session):
        self.session = session

    def create_Appointment(self, params):
        new_appt = Appointment(**params)
        try:
            self.session.add(new_appt)
            self.session.flush()
            self.session.commit()
        except Exception as err:
            print('DB Exception: ', err)
        return new_appt.id

    def get_Appointment_by_ID(self, id):
        resp = {}
        try:
            appt = self.session.query(Appointment)\
                .filter_by(status=True, id=id).first()
            if appt:
                resp = appt.to_dict()
        except Exception as err:
            print('DB Exception: ', err)
        return resp

    def get_Appointments(self, **params):
        resp = []
        try:
            appts = self.session.query(Appointment)\
                .filter_by(status=True, **params).all()
            if appts:
                resp = [i.to_dict() for i in appts]
        except Exception as err:
            print('DB Exception: ', err)
        return resp

    def get_Appointments_by_Date_Range(self, date_from, date_to):
        resp = []
        try:
            appts = self.session.query(Appointment).filter(
                    and_(Appointment.date >= date_from,
                         Appointment.date <= date_to)).all()
            if appts:
                resp = [i.to_dict() for i in appts]
        except Exception as err:
            print('DB Exception: ', err)
        return resp

    def update_Appointment(self, id, params):
        status = True
        try:
            self.session.query(Appointment)\
                .filter_by(id=id, status=True).update(params)
            self.session.commit()
        except Exception as err:
            print('DB Exception: ', err)
            status = False
        return status

    # NOTE: No true DELETE
    def delete_Appointment(self, id):
        status = True
        try:
            Appointment.query.filter_by(id=id).delete()
            self.session.commit()
        except Exception as err:
            print('DB Exception: ', err)
            status = False
        return status

    # User
    def create_User(self, params):
        new_user = User(**params)
        try:
            self.session.add(new_user)
            self.session.flush()
            self.session.commit()
        except Exception as err:
            print('DB Exception: ', err)
        return new_user.id

    def get_User(self, username):
        resp = {}
        try:
            user = self.session.query(User)\
                .filter_by(username=username).first()
            if user:
                resp = user.to_dict()
        except Exception as err:
            print('DB Exception: ', err)
        return resp

    def get_User_by_ID(self, id):
        resp = {}
        try:
            user = self.session.query(User).filter_by(id=id).first()
            if user:
                resp = user.to_dict()
        except Exception as err:
            print('DB Exception: ', err)
        return resp

from db_model import db, User, Appointment
from sqlalchemy import and_


session = db.session


def create_Appointment(params):
    try:
        new_appt = Appointment(**params)
        session.add(new_appt)
        session.flush()
        session.commit()
    except Exception as err:
        print('DB Exception: ', err)
    return new_appt.id

def get_Appointment_by_ID(id):
    resp = {}
    try:
        appt = Appointment.query.filter_by(status=True, id=id).first()
        if appt:
            resp = appt.to_dict()
    except Exception as err:
        print('DB Exception: ', err)
    return resp

def get_Appointments(**params):
    resp = []
    try:
        appts = Appointment.query.filter_by(status=True, **params).all()
        if appts:
            resp = [i.to_dict() for i in appts]
    except Exception as err:
        print('DB Exception: ', err)
    return resp

def get_Appointments_by_Date_Range(date_from, date_to):
    resp = []
    try:
        appts = Appointment.query.filter(
            and_(Appointment.date >= date_from,
                Appointment.date <= date_to)).all()
        if appts:
            resp = [i.to_dict() for i in appts]
    except Exception as err:
        print('DB Exception: ', err)
    return resp


def update_Appointment(id, params):
    status = True
    try: 
        Appointment.query.filter_by(id=id, status=True).update(params)
        session.commit()
    except Exception as err:
        print('DB Exception: ', err)
        status = False
    return status


# NOTE: No true DELETE,
# updates status to False instead
# def delete_Appointment(id):
#     status = True
#     try:
#         Appointment.query.filter_by(id=id).delete()
#         session.commit()
#     except Exception as err:
#         print('DB Exception: ', err)
#         status = False
#     return status

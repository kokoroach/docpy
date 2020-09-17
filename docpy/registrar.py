from db_model import db, User, Appointment


def create_Appointment(params):
    try:
        new_appt = Appointment(**params)
        db.session.add(new_appt)
        db.session.commit()
    except Exception as err:
        print('DB Exception: ', err)


def update_Appointments(params):
    pass


def get_Appointments(date=None):
    if date is not None:
        return Appointment.query.filter(Appointment.date == date).all()
    return Appointment.query.all()

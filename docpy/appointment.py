import registrar as reg

from datetime import date, time


# TODO: move to utilities
def is_valid_time(check_time):
    start_time = time(9)  # 9 AM
    end_time = time(17)  # 5 PM
    return start_time <= check_time <= end_time


class Appointment:

    def __init__(self, id=None, patient_name=None, date=None, from_time=None,
                 to_time=None, comment=None, **kwargs):
        self.id = id
        self.patient_name = patient_name
        self.date = date
        self.from_time = from_time
        self.to_time = to_time
        self.comment = comment

        if not self._is_valid_DateTime(date, from_time, to_time):
            raise ValueError("Invalid Date or Time of Appointment")

    @property
    def patient_name(self):
        return self._patient_name

    @patient_name.setter
    def patient_name(self, p):
        if not p:
            raise Exception("Patient cannot be empty")
        self._patient_name = p

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, d):
        if date.today() > d:
            raise Exception("Date cannot be in the Past")
        self._date = d

    @property
    def from_time(self):
        return self._from_time

    @from_time.setter
    def from_time(self, ft):
        if not is_valid_time(ft):
            raise ValueError("Time should be between 9:00 AM to 5:00 PM")
        self._from_time = ft

    @property
    def to_time(self):
        return self._to_time

    @to_time.setter
    def to_time(self, tt):
        if not is_valid_time(tt):
            raise ValueError("Time should be between 9:00 AM to 5:00 PM")
        self._to_time = tt

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, c):
        if not c:
            raise Exception("Comment cannot be empty")
        self._comment = c

    @staticmethod
    def _is_valid_DateTime(date, from_time, to_time):
        # That date is not Sunday
        if date.weekday() == 6:
            return False
        # That time from < to
        if from_time >= to_time:
            return False
        return True


class AppointmentManager:

    def __init__(self):
        pass

    def _make_appointment(self, params, resched=False):
        appt = Appointment(**params)
        if not self._is_available(appt, resched=resched):
            raise ValueError("This date and time is already booked")
        return appt

    def _is_available(self, appt, resched=False):
        for b_appt in reg.get_Appointments(date=appt.date):
            if resched and appt.id == b_appt['id']:
                continue
            if b_appt['from_time'] <= appt.from_time <= b_appt['to_time']:
                return False
            if b_appt['from_time'] <= appt.to_time <= b_appt['to_time']:
                return False
        return True

    def create_Appointment(self, params, user_id):
        appt = self._make_appointment(params)
        params = {key.lstrip('_'): getattr(appt, key) for key in vars(appt)}
        params['user_id'] = user_id
        return reg.create_Appointment(params)

    def update_Appointment(self, appt_id, params, user_id):
        attrs = reg.get_Appointment_by_ID(appt_id)
        if attrs['user_id'] != user_id:
            raise Exception("Permission denied")
        attrs.update(params)
        self._make_appointment(attrs, resched=True)
        return reg.update_Appointment(appt_id, params)

    def delete_Appointment(self, appt_id, user_id):
        params = {'status': False}
        return self.update_Appointment(appt_id, params, user_id)

    def get_Appointments_by_Range(self, date_from, date_to):
        if date_from > date_to:
            raise ValueError("Provide correct date range")
        return reg.get_Appointments_by_Date_Range(date_from, date_to)


if __name__ == '__main__':
    def create_Users():
        admin = User(username='admin')
        guest = User(username='guest')

        db.session.add(admin)
        db.session.add(guest)
        db.session.commit()
        
    # TODO:  # Assert db creation
    from db_model import db, User
    db.create_all()

    date_today = date.today()
    from_time = time(10, 0)
    to_time = time(11, 1)

    create_Users()

    # New Appointment
    params = {
        "patient_name": "Patient 1",
        "date": date_today,
        "from_time": from_time,
        "to_time": to_time,
        "comment": "Comment Here"
    }

    user_id = 1

    # Creation of Appointment
    manager = AppointmentManager()
    appt_id = manager.create_Appointment(params, user_id)

    # # Edit of Appointment
    updates = {
        "from_time": time(9, 0),
    }

    # print('UPDATE')
    # manager.update_Appointment(appt_id, updates, user_id)
    # r = reg.get_Appointment_by_ID(appt_id)
    # print(r)

    # print('DELETE')
    # manager.delete_Appointment(appt_id, user_id)
    # r = reg.get_Appointment_by_ID(appt_id)
    # print(r)

    # print('GET')
    # date_from = date_today
    # date_to = date(2020, 9, 19)
    # r = manager.get_Appointments_by_Range(date_from, date_to)
    # print(r)

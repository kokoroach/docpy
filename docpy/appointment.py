import registrar as reg

from datetime import date, time


# TODO: move to utilities
def is_valid_time(check_time):
    start_time = time(9)  # 9 AM
    end_time = time(17)  # 5 PM
    return start_time <= check_time <= end_time


class Appointment:

    def __init__(self, patient_name=None, date=None, from_time=None,
                 to_time=None, comment=None):
        if not self._is_valid_DateTime(date, from_time, to_time):
            raise ValueError("Invalid Date or Time of Appointment")
        self.patient_name = patient_name
        self.date = date
        self.from_time = from_time
        self.to_time = to_time
        self.comment = comment

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

    def create_Appointment(self, appt):
        if not isinstance(appt, Appointment):
            raise ValueError("Argument must be of type 'Appointment'")
        if not self._is_available(appt):
            raise ValueError("This date and time is already booked")
        params = {key.lstrip('_'): getattr(appt, key) for key in vars(appt)}
        params['user_id'] = 1  # TODO: Provide better implementation for UserID Logic
        reg.create_Appointment(params)

    def edit_Appointment(appt):
        pass

    def delete_Appointment():
        pass

    def get_Appointments():
        pass

    def _is_available(self, appt):
        for b_appt in reg.get_Appointments(appt.date):
            if b_appt.from_time <= appt.from_time <= b_appt.from_time:
                return False
            if b_appt.from_time <= appt.to_time <= b_appt.from_time:
                return False
        return True


def create_Users():
    admin = User(username='admin')
    guest = User(username='guest')

    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()


if __name__ == '__main__':
    # TODO:  # Assert db creation
    from db_model import db, User
    db.create_all()

    date_today = date.today()
    from_time = time(10, 0)
    to_time = time(11, 1)

    create_Users()

    # New Appointment
    appt_1 = Appointment(
        patient_name='Patient 1',
        date=date_today,
        from_time=from_time,
        to_time=to_time,
        comment='asd'
    )

    # Creation of Appointment
    manager = AppointmentManager()
    manager.create_Appointment(appt_1)
    manager.create_Appointment(appt_1)

    # Edit of Appointment
    appt_id = 1
    # manager.create_Appointment(appt_id, updates)

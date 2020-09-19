import utils
from db import session
from datetime import date as Date, time as Time
from registrar import Registrar


reg = Registrar(session)


# TODO: move to utilities
def is_valid_time(check_time):
    start_time = Time(9)  # 9 AM
    end_time = Time(17)  # 5 PM
    return start_time <= check_time <= end_time


class Appointment:

    def __init__(self, id=None, patient_name=None, date=None, from_time=None,
                 to_time=None, comment=None, user_id=None, **kwargs):
        if isinstance(date, str):
            date = utils.date_from_str(date)
        if isinstance(from_time, str):
            from_time = utils.time_from_str(from_time)
        if isinstance(to_time, str):
            to_time = utils.time_from_str(to_time)

        self.id = id
        self.user_id = user_id
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
        if utils.get_now().date() > d:
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
        # That from_time > now
        if from_time > utils.get_now().time():
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

    def create_Appointment(self, params):
        appt = self._make_appointment(params)
        _user = reg.get_User_by_ID(params['user_id'])
        if not _user or params['user_id'] != _user['id']:
            raise Exception("Invalid User")
        params = utils.get_attribs(vars(appt))
        id = reg.create_Appointment(params)
        if not id:
            raise ValueError("Payload input error")
        return id

    def update_Appointment(self, appt_id, params, user_id):
        appt_info = reg.get_Appointment_by_ID(appt_id)
        if appt_info['user_id'] != user_id:
            raise Exception("Permission denied")
        appt_info.update(params)
        self._make_appointment(appt_info, resched=True)
        return reg.update_Appointment(appt_id, params)

    def delete_Appointment(self, appt_id, user_id):
        params = {'status': False}
        return self.update_Appointment(appt_id, params, user_id)

    def get_Appointments_by_Range(self, date_from, date_to):
        if date_from > date_to:
            raise ValueError("Provide correct date range")
        return reg.get_Appointments_by_Date_Range(date_from, date_to)


class User:

    def __init__(self, id=None, username=None, **kwargs):
        self.id = id
        self.username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, n):
        if not n:
            raise Exception("Username cannot be empty")
        self._username = n


class UserManager:

    def __init__(self):
        pass

    def create_User(self, params):
        username = params['username']
        self._check_if_exists(username)

        user = User(**params)
        params = utils.get_attribs(vars(user))
        return reg.create_User(params)

    def get_User_by_ID(self, id):
        return reg.get_User_by_ID(id)

    def get_User(self, username):
        return reg.get_User(username)

    def _check_if_exists(self, username):
        user = self.get_User(username)
        if user:
            raise ValueError("Username already taken")

if __name__ == "__main__":
    manager = UserManager()
    data = {'username': 'asd'}
    manager.create_User(data)
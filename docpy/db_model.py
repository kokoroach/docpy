from datetime import datetime, date, time

from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Date, Time


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False) # TODO
    created_date = db.Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<User %r>' % self.username


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(80), nullable=False)
    date = db.Column(Date, nullable=False)
    from_time = db.Column(Time, nullable=False)
    to_time = db.Column(Time, nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    # created_on = db.Column(DateTime, default=datetime.datetime.utcnow, # TODO
    #                        nullable=False)
    # edited_on = db.Column(DateTime, nullable=False) # TODO

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '{} @ {} - {}'.format(self.date, self.from_time, self.to_time)


# ---------------------------------
# BASE TESTS


def create_Users():
    admin = User(username='admin')
    guest = User(username='guest')

    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()


def create_Appointments(user_id):
    date_today = date.today()
    from_time = time(0, 0)
    to_time = time(1, 1)

    appt_1 = Appointment(
        patient_name='Patient 1', date=date_today, from_time=from_time,
        to_time=to_time, comment='asd', user_id=user_id)
    appt_2 = Appointment(
        patient_name='Patient 2', date=date_today, from_time=from_time,
        to_time=to_time, comment='asdasd', user_id=user_id)

    db.session.add(appt_1)
    db.session.add(appt_2)
    db.session.commit()


if __name__ == '__main__':
    # from yourapplication import db
    db.create_all()

    create_Users()
    q = User.query.filter(User.username == 'admin').first()

    create_Appointments(user_id=q.id)
    print(Appointment.query.all())

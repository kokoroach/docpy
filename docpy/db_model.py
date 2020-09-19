from datetime import datetime, date, time
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Date, Time, String, Integer, Boolean, Column


Base = declarative_base()


class ModelMixin:

    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = []
        elif not isinstance(exclude, list):
            raise TypeError('Exclude must be list')
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude}


class User(Base, ModelMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    # email = Column(String(120), unique=True, nullable=False) # TODO
    created_date = Column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '{}'.format(self.username)


class Appointment(Base, ModelMixin):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    patient_name = Column(String(80), nullable=False)
    date = Column(Date, nullable=False)
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)
    comment = Column(String(100), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    # created_on = Column(DateTime, default=datetime.datetime.utcnow, # TODO
    #                        nullable=False)
    # edited_on = Column(DateTime, nullable=False) # TODO

    user_id = Column(
        Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '{} @ {}-{}'.format(self.date, self.from_time, self.to_time)

    def to_dict(self):
        return super(Appointment, self).to_dict(exclude=['status'])

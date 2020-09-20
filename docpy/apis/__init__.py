try:
    import werkzeug
    werkzeug.cached_property
except AttributeError:
    werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Blueprint
from flask_restplus import Api

from .user import api as user_ns
from .appointment import api as appt_ns
# from ..docpy import __version__ as version


API_BASE = '/api/v0'

blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    # version=version, 
    title="DocPy APIs",
    description="API for Doctor's Appointment",
)

api.add_namespace(user_ns)
api.add_namespace(appt_ns)

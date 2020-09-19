from docpy import __version__


def test_version():
    assert __version__ == '0.1.0'


# Create User
def test_create_user():
    pass

def test_create_existing_user():
    pass


# Create Appointment
def test_create_appointment():
    pass

def test_create_existing_appointment():
    pass

def test_create_appointment_date_is_sunday():
    pass

def test_create_appointment_date_is_past():
    pass

def test_create_appointment_invalid_from_time():
    pass

def test_create_appointment_invalid_to_time():
    pass

def test_create_appointment_time_is_past():
    pass


# Update Appointment
def test_update_appointment():
    pass

def test_update_appointment_date_is_sunday():
    pass

def test_update_appointment_date_is_past():
    pass

def test_update_appointment_invalid_from_time():
    pass

def test_update_appointment_invalid_to_time():
    pass

def test_create_appointment_time_is_past():
    pass

def test_update_appointment_not_of_user():
    pass


# Delete Appointment
def test_delete_appointment_invalid_to_time():
    pass

def test_create_appointment_time_is_past():
    pass

def test_update_appointment_not_of_user():
    pass


# Get Appointment
def test_get_appointment():
    pass

def test_get_appointment_invalid_past_date():
    pass

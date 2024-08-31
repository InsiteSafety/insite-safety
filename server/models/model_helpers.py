from sqlalchemy import Time 
from config import db

MAX_NAME_LENGTH = 100
"""
The maximum number of characters set for a name attribute of a model.
"""

MAX_EMAIL_LENGTH = 254
"""
The maximum number of characters set for an email attribute of a model.
"""

MAX_INPUT_LENGTH = 260
"""
The maximum number of characters set for a string-type model attribute that is
not for a name or email.
"""

def validate_model_input_string(key, name, max_length):
    """
    Checks if a given name for an attribute of a model is a non-empty
    string whose length is no more than the maximum number of characters
    set for the model classes.

    Args:
        key (str): the attribute name.
        name (str): the attribute value.
        max_length (int): the maximum string length.

    Raises:
        ValueError: if the name is None or the length is greater than the limit.
    """
    
    if not name:
        raise ValueError(f"{key.title()} field is required.")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"{key.title()} field must be {max_length} characters or less.")
    
def validates_model_input_datetime(key, value, name, self):
    if not isinstance(value, db.DateTime):
        raise TypeError(f"{key} must be a DateTime object")
    now = db.DateTime.now()
    if value == isinstance(db.DateTime):
        if value > now: 
            raise ValueError(f"{key} cannot be set in the future")
    if key.startswith("report"):
        incident_datetime = self.incident_date + self.incident_time
        if key == 'report_date':
            report_datetime = value + Time(0, 0, 0)
        else: 
            report_datetime = value
        if report_datetime <= incident_datetime:
            raise ValueError("Report DateTime must be after incident or near_miss DateTime")
        
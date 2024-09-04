from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

from config import db
from models.model_helpers import MAX_NAME_LENGTH, validate_model_input_string, MAX_INPUT_LENGTH, validates_model_input_datetime

# Validations To Do
# incident_date, incident_time, incident_report_date, incident_report_time


class Incident(db.Model, SerializerMixin):
    """
    TODO
    """

    __tablename__ = 'incidents'

    id = db.Column(db.Integer, primary_key=True)
    injury_description = db.Column(db.String(MAX_INPUT_LENGTH))
    incident_date = db.Column(db.DateTime, nullable=False)
    incident_time = db.Column(db.DateTime, nullable=False)
    report_date = db.Column(db.DateTime, nullable=False)
    report_time = db.Column(db.DateTime, nullable=False)
    mechansim_of_injury = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)
    body_part_injured = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)
    symptoms = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)
    incident_location = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    risk_assessment_severity = db.Column(db.Integer, nullable=False)
    risk_assessment_probability = db.Column(db.Integer, nullable=False)
    first_aid_given = db.Column(db.Boolean, nullable=False)
    first_aid_details = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)
    recovery_status = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)
    pain_level = db.Column(db.Integer())
    
    # Foreign Keys: 
     
    # ✅ user_id (one user to many incidents)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='incidents')
    
    # ✅ employee_id: one to many

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    employee = db.relationship('Employee', back_populates='incidents')

    # medical records 
    # company_id
    # Pain level constrant disallowing more than two characters. Validations will ensure users can only choose vlaues between 0 and 10. 

    @validates('injury_description', 'mechanism_of_injury', 'body_part_injured', 'symptoms', 'incident_location', 'first_aid_details', 'recovery_status')
    def validate_name(self, key, name):
        """
        Validates that the 'injury_description', 'mechanism_of_injury', 'body_part_injured', 'symptoms', 'incident_location', 'first_aid_details', 'recovery_status' attributes are all non-empty strings that are at most 260 characters long.

        Args:
            key (str): the attribute name.
            name (str): the attribute value.

        Returns:
            str: the attribute value.
        """
        validate_model_input_string(key, name, MAX_INPUT_LENGTH)
        return name
    
    @validates('risk_assessment_severity', 'risk_assessment_probability')
    def validate_value(self, key, value):
        if value is None:
            raise ValueError(f'{key} must be between one and three')
        if not isinstance(value, int):
            return "value must be an integer"
        if value > 3:
            raise ValueError(f'{key} must be between one and three')
        if value < 1:
            raise ValueError(f'{key} must be between one and three')
        return value
    
    @validates('pain_level')
    def validate_pain_level(self, key, value):
        """
    Validates that pain_level is an integer between 0 and 10.

    Args:
        key (str): the attribute name.
        value (int): the attribute value.

    Returns:
        int: the validated value.

    Raises:
        ValueError: If the value is outside the range 0-10.
    """
        if value is None:
            raise ValueError(f'{key} cannot be null')
        if not isinstance(value, int):
            raise TypeError(f'{key} must be an integer')
        if value < 0 or value > 10:
            raise ValueError(f'{key} must be between zero and ten')
        return value
    
    @validates('incident_date', 'incident_time', 'report_date', 'report_time')
    def validate_DateTime_fields(self, key, value):
        """
        Validates that DateTime fields are not set in the future and that
        the report DateTime is after the incident DateTime.

        Args:
            key (str): The attribute name being validated.
            value (DateTime): The value of the attribute.

        Returns:
            DateTime: The validated value.

        Raises:
            ValueError: If the DateTime is in the future or if the report DateTime precedes the incident DateTime.
        """
        validates_model_input_datetime(self, key, value)
        return value


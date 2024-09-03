from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import db
from models.model_helpers import MAX_NAME_LENGTH, MAX_INPUT_LENGTH, validate_model_input_string, validates_model_input_datetime

class Near_miss(db.Model, SerializerMixin):
    """
    TODO
    """ 

    __tablename__ = 'near_misses'

    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.DateTime, nullable=False)
    report_time = db.Colimn(db.DateTime, nullable=False)
    near_miss_date = db.Column(db.DateTime, nullable=False) 
    near_miss_time = db.Column(db.DateTime, nullable=False) 
    location = db.Column(db.String, nullable=False)
    description = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)

    # 1. reported_by_user_id (one user can report many nm)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates="near_misses")

    # 2. Near Miss (one comapny with many near misses)
    company_id = db.Column(db.Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='companies')

    # 2. root_cause_analysis_id (one rca to one near miss)
        
    # 3. corrective_action_id (many corrective actions to one near_miss)

    @validates('location', 'desciption')
    def validate_location(self, key, name):
        """
        Validates that 'location' attribute is a non-empty string at most 260 characters long.

        Args: 
            key (str): the attribute name.
            name (str): the attribute value.

        Returns: 
            str: the attribute value.

        """
        validate_model_input_string(key, name, MAX_INPUT_LENGTH)
        return name
    
    @validates('near_miss_date', 'near_miss_time', 'report_date', 'report_time')
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



from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config import db
from models.model_helpers import MAX_NAME_LENGTH, MAX_INPUT_LENGTH, validate_model_input_string

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

    #Foreign Relationships
        # 1. reported_by_user_id (one user can report many nm)
        # 2. root_cause_analysis_id (one rca to one near miss)
        # 3. corrective_action_id (many corrective actions to one near_miss)

    @validates('location')
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
                
        if not isinstance(value, db.Datetime):
            raise TypeError(f'{key} must be a DateTime object')
        now = db.DateTime.now()
        if value > now:
            raise TypeError(f'{key} cannot be set in the future')
        if key.startswith('report_date') and hasattr(self, 'near_miss_date'):
            near_miss_DateTime = getattr(self, 'near_miss_date')
            if value <= near_miss_DateTime:
                raise ValueError('report DateTime must be after near_miss_DateTime')
        return value



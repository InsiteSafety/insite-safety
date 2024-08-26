from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db
from models.model_helpers import *

class Employee(db.Model, SerializerMixin):
    """
    TODO
    """
    
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    last_name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    department = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    position = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    
    # Foreign Key
    # incident_id
    
    @validates('first_name', 'last_name', 'department', 'position')
    def validate_name(self, key, name):
        """
        Validates that the first_name, last_name, department, and position
        attributes are all non-empty strings that are at most 100 characters long.

        Args:
            key (str): the attribute name.
            name (str): the attribute value.

        Returns:
            str: the attribute value.
        """
        
        validate_model_input_string(key, name, MAX_NAME_LENGTH)
        return name
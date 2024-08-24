from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from config import db
from model_helpers import MAX_NAME_LENGTH, MAX_INPUT_LENGTH, validate_model_input_string

class Company(db.Model, SerializerMixin):
    """
    TODO
    """
    
    __tablename__ = 'companies'
    
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    address = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)
    
    # Foreign Keys
    # industry_id
    # insection_id
    
    def __repr__(self):
        pass
    
    @validates('name')
    def validate_name(self, key, name):
        """
        Validates that the company name is a non-empty string that is at most
        100 characters long.

        Args:
            key (str): the attribute name.
            name (str): the attribute value.

        Returns:
            str: the attribute value.
        """
        validate_model_input_string(key, name, MAX_NAME_LENGTH)
        return name
    
    @validates('address')
    def validate_address(self, key, address):
        """
        Validates that the company name is a non-empty string that is at most
        260 characters long.

        Args:
            key (str): the attribute name.
            name (str): the attribute value.

        Returns:
            str: the attribute value.
        """
        validate_model_input_string(key, address, MAX_INPUT_LENGTH)
        return address
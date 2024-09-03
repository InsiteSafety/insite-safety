from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey
from models.user import User

from config import db
from models.model_helpers import MAX_NAME_LENGTH, MAX_INPUT_LENGTH, validate_model_input_string

class Company(db.Model, SerializerMixin):
    """
    TODO
    """
    
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    address = db.Column(db.String(MAX_INPUT_LENGTH), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    # ✅ Foreign Keys (many users to one company)
    user = relationship("User", back_populates="companies")
    
    # industry_id: 

    # ✅ Company (many near misses to one company)
    near_misses = relationship('Near_miss', back_populates='companies')

    # inspection_id?
    
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
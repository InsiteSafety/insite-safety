from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt
from server.models.model_helpers import MAX_NAME_LENGTH, MAX_EMAIL_LENGTH, validate_model_input_string

print('Testing')

class User(db.Model, SerializerMixin):
    """
    Person that is physically using the application, Insite Safety.
    TODO
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(MAX_NAME_LENGTH), nullale=False)
    last_name = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    username = db.Column(db.String(MAX_NAME_LENGTH), nullable=False)
    email = db.Column(db.String(MAX_EMAIL_LENGTH), nullable=False)

    # Foreign Keys
    # company - one to one 
    company = relationship('Company', back_populates='user_id', uselist=False)
    # incidents - one to many

    _password_hash = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'\n<User id={self.id} first_name={self.first_name} last_name={self.last_name} username={self.username} email={self.email}'
    
    @validates('first_name', 'last_name')
    def validate_name(self, key, name):
        """
        Validates that the first and last names are non-empty strings that are at
        most 100 characters long.

        Args:
            key (str): the attribute name.
            name (str): the attribute value.

        Returns:
            str: the first or last name.
        """
        validate_model_input_string(key, name, MAX_NAME_LENGTH)
        return name
    
    @validates('username')
    def validate_username(self, key, username):
        """
        Validates that the username is a non-empty string that is at most 100
        characters long.

        Args:
            key (str): the attribute name (should be username).
            username (str): the username attribute value.

        Raises:
            ValueError: if the username is NOT unique.

        Returns:
            str: the username.
        """
        validate_model_input_string(key, username, MAX_NAME_LENGTH)
        username_exists = db.session.query(User).filter(User.username == username).first()
        if username_exists:
            raise ValueError('username must be unique')
        return username
    
    @validates('email')
    def validates_email(self, key, email):
        """
        Validates that the email is a valid, unique email address.

        Args:
            key (str): the attribute name.
            email (str): the email attribute value.

        Raises:
            ValueError: If the input is not of type email or a user with the email already exists.

        Returns:
            str: the email.
        """
        validate_model_input_string(key, email, MAX_EMAIL_LENGTH)
        if (not email) or ('@' not in email) :
            raise ValueError('Email is required.')
        email_exists = db.session.query(User).filter(User.email == email).first()
        if email_exists:
            raise ValueError('Email must be unique.')
        return email

    @hybrid_property
    def password_hash(self):
        """Restriction for user. Prevents user from accessing password hash.

        Raises:
            AttributeError: if an attempt to access the password hash has been made.
        """
        
        raise AttributeError('password hashes may not be viewed')
    
    @password_hash.setter
    def password_hash(self, password):
        """Sets a new password for user and rehashes it.

        Args:
            password (str): the new password.
        """
        
        bcrypt_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.password_hash = bcrypt_hash

    def authenticate(self, password):
        """Check if user entered the correct password.

        Args:
            password (str): the password

        Returns:
            bool: if user entered the correct password; False otherwise.
        """
        
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f'User: {self.username}, ID: {self.id}'
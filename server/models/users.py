from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

class User(db.Model, SerializerMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullale=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    # Foreign Keys
    # user_role = db.Column(db.String)
    # company
    # submitted_incidents 

    _password_hash = db.Column(db.String, nullable=False)
    def __repr__(self):
        return f'\n<User id={self.id} first_name={self.first_name} last_name={self.last_name} username={self.username} email={self.email}'
    
    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name:
            raise ValueError('first_name field is required')
        if key == 'first_name':
            if len(first_name) >= 100:
                raise ValueError('first_name must be 100 characters or less')
        return first_name 
    
    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name:
            raise ValueError('last_name field is required')
        if key == 'last_name':
            if len(last_name) >= 100:
                raise ValueError('last_name must be 100 characters or less')
        return last_name
    
    @validates('username')
    def validate_username(self, key, username):
        username_exists = db.session.query(User).filter(User.username == username).first()
        if not username:
            raise ValueError('username field is required')
        if username_exists:
            raise ValueError('username must be unique')
        elif key == 'username':
            if len(username) >= 100:
                raise ValueError('username must be 100 characters or less')
        return username
    
    @validates('email')
    def validates_email(self, key, email):
        email_exists = db.session.query(User).filter(User.email == email).first()
        if not email :
            raise ValueError('email is required')
        if email_exists:
            raise ValueError('email must be 100 characters or less')
        return email

    @hybrid_property
    def password_hash(self):
        raise Exception('password hashes may not be viewed')
    
    @password_hash.setter
    def password_hash(self, password):
        bcrypt_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.password_hash = bcrypt_hash

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f'User: {self.username}, ID: {self.id}'
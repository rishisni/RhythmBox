from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_creator = db.Column(db.Boolean, default=False)  

    def __init__(self, username, email, password, is_admin=False, is_creator=False): 
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_creator = is_creator

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'is_creator')

# Initialize Marshmallow schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)

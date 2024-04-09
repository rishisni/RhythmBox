from dataclasses import fields
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

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


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    cover_photo = db.Column(db.String(200), nullable=True)  # Path to cover photo
    song_count = db.Column(db.Integer, default=0)
    # Relationship with Song
    # songs = db.relationship('Song', backref='album', lazy=True)

    def __repr__(self):
        return f"Album('{self.name}', '{self.artist}', '{self.date_added}')"
class AlbumSchema(ma.Schema) :
    class Meta:
        fields = ('id','name','artist','date_added','cover_photo','song_count')

album_schema = AlbumSchema
albums_schema = AlbumSchema(many=True)       
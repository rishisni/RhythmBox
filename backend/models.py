from dataclasses import fields
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_creator = db.Column(db.Boolean, default=False)
    songs = relationship('Song', backref='user')
     
    def __init__(self, username, email, password, is_admin=False, is_creator=False): 
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_creator = is_creator

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin', 'is_creator')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    song_count = db.Column(db.Integer, default=0)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', backref='album', lazy=True)
    user = db.relationship('User', backref='albums')  
    songs = db.relationship('Song', backref='album', lazy=True,cascade='all, delete-orphan')
    photo_data = db.Column(db.LargeBinary, nullable=True)  
    photo_filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Album('{self.name}', '{self.artist}', '{self.date_added}')"

class AlbumSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'artist', 'date_added', 'song_count', 'photo_filename', 'user_id')

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lyrics = db.Column(db.Text, nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(20), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    audio_data = db.Column(db.LargeBinary, nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Song('{self.name}', '{self.album_id}', '{self.date_created}')"

class SongSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'lyrics', 'genre', 'duration', 'date_created',  'album_id', 'user_id')

song_schema = SongSchema()
songs_schema = SongSchema(many=True)
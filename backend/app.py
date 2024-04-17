from flask import Flask, request, jsonify,send_from_directory
from werkzeug.security import generate_password_hash
from models import *
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash
from sqlalchemy import or_,func,desc
import os
import uuid
from datetime import timedelta
import base64
from sqlalchemy.orm import joinedload
from flask_redis import FlaskRedis
from celery import Celery
from config import Config
from tasks import celery

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
# app.config['REDIS_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

db.init_app(app)
redis_store = FlaskRedis(app)
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)


jwt = JWTManager(app)


migrate = Migrate(app, db)

# Configuration for Blackinstis the Token
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]


blacklisted_tokens = set()





# ------------------------------------Routes---------------------------------------------------------------------------





# Route to fetch top 3 recently added songs

@app.route('/songs/top', methods=['GET'])
def get_top_songs():
    top_songs = Song.query.options(joinedload(Song.album)).order_by(Song.date_created.desc()).limit(3).all()
    if top_songs:
        serialized_top_songs = [{
            'id': song.id,
            'name': song.name,
            'albumId': song.album.id,
            'albumName': song.album.name if song.album else 'Unknown Album'
        } for song in top_songs]
        return jsonify({'top_songs': serialized_top_songs}), 200
    else:
        return jsonify({'message': 'No songs found'}), 404

@app.route('/songs/top-liked', methods=['GET'])
def get_top_liked_songs():
    top_liked_songs = Song.query \
        .join(Like, Song.id == Like.song_id) \
        .group_by(Song.id) \
        .order_by(desc(func.count(Like.id))) \
        .limit(3) \
        .all()

    if top_liked_songs:
        serialized_top_liked_songs = [{
            'id': song.id,
            'name': song.name,
            'albumId': song.album.id,
            'albumName': song.album.name if song.album else 'Unknown Album'
        } for song in top_liked_songs]
        return jsonify({'top_liked_songs': serialized_top_liked_songs}), 200
    else:
        return jsonify({'message': 'No songs found'}), 404

# Route For User and Creator Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_creator = data.get('is_creator', False)
    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()
    if existing_user or existing_email:
        return jsonify({'message': 'Username or email already exists'}), 400
    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        is_creator=is_creator
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# Route For User and Creator Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username_or_email = data.get('usernameOrEmail')
    password = data.get('password')
    user = User.query.filter(
        or_(User.username == username_or_email, User.email == username_or_email)).first()
    if user:
        if user.is_admin:
            return jsonify({'message': 'Admin login should be done through a separate form'}), 401
        if check_password_hash(user.password, password):
            # Update the last_visit field when the user logs in
            user.update_last_visit()
            db.session.commit()  # Commit the changes to the database
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token, 'profile_url': '/profile'}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404


# Route For Admin Login
@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    username_or_email = data.get('usernameOrEmail')
    password = data.get('password')
    user = User.query.filter(
        or_(User.username == username_or_email, User.email == username_or_email)).first()
    if user:
        if user.is_admin:

            if check_password_hash(user.password, password):

                access_token = create_access_token(identity=user.id)
                return jsonify({'access_token': access_token, 'profile_url': '/profile'}), 200
            else:
                return jsonify({'message': 'Invalid username or password'}), 401
        else:
            return jsonify({'message': 'Unauthorized access'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404


# Route to Get User Role
@app.route('/user-role', methods=['GET'])
@jwt_required()
def get_user_role():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({'is_admin': user.is_admin, 'is_creator': user.is_creator}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


# Route For Profile
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({'username': user.username, 'email': user.email}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


# Function for Blockist Loader
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, decoded_token):
    jti = decoded_token["jti"]
    return jti in blacklisted_tokens


#Route to Add Song
@app.route('/add-album', methods=['POST'])
@jwt_required()
def add_album():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.is_admin or user.is_creator:
        data = request.form
        name = data.get('name')
        artist = data.get('artist')
        
        if 'photo' not in request.files:
            return jsonify({'message': 'No photo uploaded'}), 400

        photo = request.files['photo']
        
        if photo.filename == '':
            return jsonify({'message': 'No selected photo'}), 400

        _, ext = os.path.splitext(photo.filename)
        unique_filename = str(uuid.uuid4()) + ext

        photo_data = photo.read()

        new_album = Album(name=name, artist=artist, user=user, photo_data=photo_data, photo_filename=unique_filename)
        db.session.add(new_album)
        db.session.commit()

        return jsonify({'message': 'Album added successfully'}), 201
        
    else:
        return jsonify({'message': 'Unauthorized to add albums'}), 403

    

# Route For Fetching Albums Created by the Current User
@app.route('/albums', methods=['GET'])
@jwt_required()
def get_albums():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.is_admin or user.is_creator:

        albums = Album.query.filter_by(user_id=current_user_id).all()

        if albums:

            serialized_albums = [{
                'id': album.id,
                'name': album.name,
                'artist': album.artist,
                'song_count': album.song_count,
                'photo_data': base64.b64encode(album.photo_data).decode(),  
            } for album in albums]
            return jsonify(serialized_albums), 200
        else:
            return jsonify({'message': 'No albums found for the current user'}), 404
    else:
        return jsonify({'message': 'Unauthorized to access albums'}), 403

# Route For Fetching All Albums
@app.route('/albums/all', methods=['GET'])
@jwt_required()
def get_all_albums():
    albums = Album.query.order_by(Album.id.desc()).all()
    if albums:

        serialized_albums = [{
            'id': album.id,
            'name': album.name,
            'artist': album.artist,
            'song_count': album.song_count,
            'photo_data': base64.b64encode(album.photo_data).decode(), 
            'created_by': {
                'id': album.user.id,
                'username': album.user.username
            }
        } for album in albums]
        return jsonify(serialized_albums), 200
    else:
        return jsonify({'message': 'No albums found'}), 404


# Route to Edit Album
@app.route('/albums/<int:album_id>', methods=['PUT','GET'])
@jwt_required()
def edit_album(album_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    album = Album.query.get(album_id)

    if not album:
        return jsonify({'message': 'Album not found'}), 404

    if user.id != album.user_id:
        return jsonify({'message': 'Unauthorized to edit this album'}), 403

    data = request.json
    name = data.get('name')
    artist = data.get('artist')

    album.name = name
    album.artist = artist

    db.session.commit()

    return jsonify({'message': 'Album updated successfully'}), 200


# Route For Deleting an Album
@app.route('/albums/<int:album_id>', methods=['DELETE'])
@jwt_required()
def delete_album(album_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    album = Album.query.get(album_id)

    if not album:
        return jsonify({'message': 'Album not found'}), 404

    if user.id != album.user_id:
        return jsonify({'message': 'Unauthorized to delete this album'}), 403

    

    db.session.delete(album)
    db.session.commit()

    return jsonify({'message': 'Album deleted successfully'}), 200



@app.route('/albums/<int:album_id>/add-song', methods=['POST'])
@jwt_required() 
def add_song(album_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    album = Album.query.get(album_id)

    if user and album:
        data = request.form
        name = data.get('name')
        lyrics = data.get('lyrics')
        genre = data.get('genre')
        duration = data.get('duration')
        song_data = request.files['song_file'].read()  
        new_song = Song(name=name, lyrics=lyrics, genre=genre,
                        duration=duration, audio_data=song_data, album=album, user_id=user.id)
        db.session.add(new_song)
        album.song_count += 1
        db.session.commit()

        return jsonify({'message': 'Song added successfully'}), 201
    else:
        return jsonify({'message': 'Unauthorized or Album not found'}), 403


@app.route('/albums/<int:album_id>/songs', methods=['GET'])
@jwt_required() 
def get_album_songs(album_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    album = Album.query.get(album_id)
    if album:
        songs = Song.query.filter_by(album_id=album_id).all()
        serialized_songs = [{
            'id': song.id,
            'name': song.name,
            'lyrics': song.lyrics,
            'genre': song.genre,
            'albumName': song.album.name,
            'duration': song.duration,
            'date_created': song.date_created,
            'like_count' : get_like_count(song.id)   ,
            'audio_data': base64.b64encode(song.audio_data).decode('utf-8') if song.audio_data else None,
            'added_by': { 'id' :song.user_id, 'username' :song.user.username}
        } for song in songs]
        return jsonify({'songs': serialized_songs, 'current_user_id': current_user_id}), 200
    else:
        return jsonify({'message': 'Album not found'}), 404


@app.route('/albums/<int:album_id>/songs/<int:song_id>', methods=['PUT'])
@jwt_required()
def edit_song(album_id, song_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    album = Album.query.get(album_id)
    song = Song.query.get(song_id)

    if not album or not song:
        return jsonify({'message': 'Album or song not found'}), 404

    if current_user_id != song.user_id:  
        return jsonify({'message': 'Unauthorized to edit this song'}), 403

    data = request.json
    name = data.get('name')
    lyrics = data.get('lyrics')
    genre = data.get('genre')
    duration = data.get('duration')

    song.name = name
    song.lyrics = lyrics
    song.genre = genre
    song.duration = duration

    db.session.commit()

    return jsonify({'message': 'Song updated successfully'}), 200


# Route for Deleting Song
@app.route('/albums/<int:album_id>/songs/<int:song_id>', methods=['DELETE'])
@jwt_required()
def delete_song(album_id, song_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    album = Album.query.get(album_id)
    song = Song.query.get(song_id)

    if not album or not song:
        return jsonify({'message': 'Album or song not found'}), 404

    if current_user_id != song.user_id: 
        return jsonify({'message': 'Unauthorized to delete this song'}), 403

    

    db.session.delete(song)
    album.song_count -= 1
    db.session.commit()

    return jsonify({'message': 'Song deleted successfully'}), 200


@app.route('/songs/all', methods=['GET'])
@jwt_required() 
def get_all_songs():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    songs = Song.query.order_by(Song.date_created.desc()).all()
    
    serialized_songs = [{
        'id': song.id,
        'name': song.name,
        'lyrics': song.lyrics,
        'artist_name': song.album.artist,  
        'duration': song.duration,
        'albumId': song.album.id,
        'date_created' : song.date_created,
        'like_count' : get_like_count(song.id)   ,
        'audio_data': base64.b64encode(song.audio_data).decode() if song.audio_data else None,
        'album_name': song.album.name if song.album else 'Unknown Album',  
    } for song in songs]
    
    return jsonify({'songs': serialized_songs}), 200


# Route For Logout
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        jti = get_jwt()["jti"]
        blacklisted_tokens.add(jti)
        user.update_last_visit()
        db.session.commit()
        return jsonify({"message": "Successfully logged out"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


# Route for Getting User Id
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200


@app.route('/create-playlist', methods=['POST'])
@jwt_required()
def create_playlist():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    name = data.get('name')

    playlist = Playlist(name=name, user_id=current_user_id)
    db.session.add(playlist)
    db.session.commit()

    return jsonify({'message': 'Playlist created successfully'}), 201

# Route for adding a song to a playlist
@app.route('/playlists/<int:playlist_id>/add-song', methods=['POST'])
@jwt_required()
def add_song_to_playlist(playlist_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'message': 'Playlist not found'}), 404

    data = request.json
    song_id = data.get('song_id')

    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found'}), 404

    if song not in playlist.songs:
        playlist.songs.append(song)
        db.session.commit()
        return jsonify({'message': 'Song added to playlist successfully'}), 200
    else:
        return jsonify({'message': 'Song already exists in the playlist'}), 400


@app.route('/playlists', methods=['GET'])
@jwt_required() 
def get_user_playlists():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlists = Playlist.query.filter_by(user_id=current_user_id).all()

    serialized_playlists = [{
        'id': playlist.id,
        'name': playlist.name,
    } for playlist in playlists]

    return jsonify({'playlists': serialized_playlists}), 200


@app.route('/playlists/<int:playlist_id>', methods=['GET'])
@jwt_required()
def get_playlist(playlist_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user_id).first()
    if not playlist:
        return jsonify({'message': 'Playlist not found'}), 404

    serialized_playlist = {
        'id': playlist.id,
        'name': playlist.name,
        'songs': [{
            'id': song.id,
            'name': song.name,
            'artist': song.album.artist,
            'duration': song.duration,
            'audio_data': base64.b64encode(song.audio_data).decode() if song.audio_data else None,
            # Add more song details as needed
        } for song in playlist.songs]
    }

    return jsonify({'playlist': serialized_playlist}), 200

@app.route('/playlists/<int:playlist_id>/songs/<int:song_id>', methods=['DELETE'])
@jwt_required()
def remove_song_from_playlist(playlist_id, song_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({'message': 'Playlist not found'}), 404

    song = Song.query.get(song_id)
    if not song:
        return jsonify({'message': 'Song not found'}), 404

    if song in playlist.songs:
        playlist.songs.remove(song)
        db.session.commit()
        return jsonify({'message': 'Song removed from playlist successfully'}), 200
    else:
        return jsonify({'message': 'Song is not in the playlist'}), 400

@app.route('/playlists/<int:playlist_id>', methods=['DELETE'])
@jwt_required()
def delete_playlist(playlist_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user_id).first()
    if not playlist:
        return jsonify({'message': 'Playlist not found'}), 404

    db.session.delete(playlist)
    db.session.commit()

    return jsonify({'message': 'Playlist deleted successfully'}), 200


@app.route('/songs/<int:song_id>/like', methods=['POST'])
@jwt_required()
def like_song(song_id):
    current_user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=current_user_id, song_id=song_id).first()
    if like:
        like.liked = True
    else:
        like = Like(user_id=current_user_id, song_id=song_id)
        db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Song liked successfully'}), 200

@app.route('/songs/<int:song_id>/unlike', methods=['POST'])
@jwt_required()
def unlike_song(song_id):
    current_user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=current_user_id, song_id=song_id).first()
    if like:
        like.liked = False
        db.session.commit()
        return jsonify({'message': 'Song unliked successfully'}), 200
    else:
        return jsonify({'message': 'Song not liked by the user'}), 404

def get_like_count(song_id):
    return Like.query.filter_by(song_id=song_id, liked=True).count()



@app.route('/songs/<int:song_id>/report', methods=['POST'])
@jwt_required()
def report_song(song_id):
    current_user_id = get_jwt_identity()
    report = Report.query.filter_by(user_id=current_user_id, song_id=song_id).first()
    if report:
        return jsonify({'message': 'Song already reported by the user'}), 400
    else:
        report = Report(user_id=current_user_id, song_id=song_id)
        db.session.add(report)
        
        # Increment the report count for the song
        song = Song.query.get(song_id)
        if song:
            if song.report_count is None:
                song.report_count = 0
            song.report_count += 1
        
        db.session.commit()
        return jsonify({'message': 'Song reported successfully'}), 201

def admin_summary():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    # Total number of users
    total_users = User.query.count()

    # Number of users who are creators
    total_creators = User.query.filter_by(is_creator=True).count()

    # Total number of albums
    total_albums = Album.query.count()

    # Total number of songs
    total_songs = Song.query.count()

    # Total number of likes
    total_likes = Like.query.filter_by(liked=True).count()

    # Total number of reports
    total_reports = Report.query.count()

    # Song-wise like count
    song_like_counts = {}
    songs = Song.query.all()
    for song in songs:
        like_count = get_like_count(song.id)
        song_like_counts[song.name] = like_count

    # Song-wise report count
    song_report_counts = {}
    for song in songs:
        report_count = song.report_count if song.report_count else 0
        song_report_counts[song.name] = report_count

    summary = {
        "total_users": total_users,
        "total_creators": total_creators,
        "total_albums": total_albums,
        "total_songs": total_songs,
        "total_likes": total_likes,
        "total_reports": total_reports,
        "song_like_counts": song_like_counts,
        "song_report_counts": song_report_counts
    }

    return summary

# Usage
@app.route('/admin-summary', methods=['GET'])
@jwt_required()
def get_admin_summary():
    summary = admin_summary()
    return jsonify(summary)

def serialize_album(album):
    return {
        'id': album.id,
        'title': album.name,
        'artist': album.artist,
        # 'genre': album.genre,
        # Add more fields to serialize as needed
    }
def serialize_song(song):
    # Check if the song has an associated album
    album_name = song.album.name if song.album else 'Unknown Album'
    
    # Check if the song has audio data
    audio_data_encoded = base64.b64encode(song.audio_data).decode() if song.audio_data else None
    
    return {
        'id': song.id,
        'name': song.name,
        'lyrics': song.lyrics,
        'artist_name': song.album.artist if song.album else None,
        'duration': song.duration,
        'albumId': song.album.id if song.album else None,
        'date_created': song.date_created,
        'like_count': get_like_count(song.id),  # Assuming get_like_count is a defined function
        'audio_data': audio_data_encoded,
        'album_name': album_name,
    }


@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    search_query = request.args.get('query')

    if not search_query:
        return jsonify({'message': 'No search query provided'}), 400

    # Perform database queries to find matching songs and albums
    song_results = Song.query.filter(
        or_(
            Song.name.ilike(f'%{search_query}%'),
            
            Song.genre.ilike(f'%{search_query}%'),
            Song.lyrics.ilike(f'%{search_query}%'),
            # Add more fields to search as needed
        )
    ).all()

    album_results = Album.query.filter(
        or_(
            Album.name.ilike(f'%{search_query}%'),
            Album.artist.ilike(f'%{search_query}%'),
            # Album.genre.ilike(f'%{search_query}%'),
            # Add more fields to search as needed
        )
    ).all()

    serialized_songs = [serialize_song(song) for song in song_results]
    serialized_albums = [serialize_album(album) for album in album_results]

    return jsonify({'songs': serialized_songs, 'albums': serialized_albums}), 200

if __name__ == '__main__':
    app.run(debug=True)

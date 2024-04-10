from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from models import *
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import check_password_hash
from sqlalchemy import or_
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
db.init_app(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

# Configuration for Blackinstis the Token
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]


blacklisted_tokens = set()


# Configuration For Image Uplaoding
UPLOAD_FOLDER = 'static/uploads/images'

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


# Configuration For Music Files
UPLOAD_SONG_FOLDER = 'static/uploads/songs'

app.config['UPLOAD_SONG_FOLDER'] = UPLOAD_SONG_FOLDER

ALLOWED_MUSIC_EXTENSIONS = {'mp3', 'wav', 'ogg'}


def allowed_music_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_MUSIC_EXTENSIONS


def generate_unique_filename(filename):
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    filename_without_extension, extension = os.path.splitext(filename)
    return f"{filename_without_extension}.{current_datetime}{extension}"


# ------------------------------------Routes---------------------------------------------------------------------------


# Route for Getting User Id
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200


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


# Route For Adding New Album with File Upload
@app.route('/add-album', methods=['POST'])
@jwt_required()
def add_album():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user.is_admin or user.is_creator:
        data = request.form
        name = data.get('name')
        artist = data.get('artist')

        # Check if the request contains a file
        if 'cover_photo' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['cover_photo']

        # Check if the file is allowed
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = generate_unique_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Create the new album with the file path
            new_album = Album(name=name, artist=artist,
                              cover_photo=file_path, user=user)
            db.session.add(new_album)
            db.session.commit()

            return jsonify({'message': 'Album added successfully'}), 201
        else:
            return jsonify({'message': 'File type not allowed'}), 400
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
                'cover_photo': f"/{app.config['UPLOAD_FOLDER']}/{album.cover_photo}",
                'song_count': album.song_count
            } for album in albums]
            return jsonify(serialized_albums), 200
        else:
            return jsonify({'message': 'No albums found for the current user'}), 404
    else:
        return jsonify({'message': 'Unauthorized to access albums'}), 403


# Route For Fetching All Albums
@app.route('/albums/all', methods=['GET'])
def get_all_albums():
    albums = Album.query.order_by(Album.id.desc()).all()
    if albums:

        serialized_albums = [{
            'id': album.id,
            'name': album.name,
            'artist': album.artist,
            'cover_photo': f"/{album.cover_photo}",
            'song_count': album.song_count,
            'created_by': {
                'id': album.user.id,
                'username': album.user.username
            }
        } for album in albums]
        return jsonify(serialized_albums), 200
    else:
        return jsonify({'message': 'No albums found'}), 404


# Route to Edit Album
@app.route('/albums/<int:album_id>', methods=['PUT'])
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

    if os.path.exists(album.cover_photo):
        os.remove(album.cover_photo)

    db.session.delete(album)
    db.session.commit()

    return jsonify({'message': 'Album deleted successfully'}), 200


# Route to Add Song
@app.route('/albums/<int:album_id>/add-song', methods=['OPTIONS', 'POST'])
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

        if 'song_file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['song_file']

        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = generate_unique_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_song = Song(name=name, lyrics=lyrics, genre=genre,
                            duration=duration, file_path=file_path, album=album, user=user)
            db.session.add(new_song)
            album.song_count += 1
            db.session.commit()

            return jsonify({'message': 'Song added successfully'}), 201
        else:
            return jsonify({'message': 'File type not allowed'}), 400
    else:
        return jsonify({'message': 'Unauthorized or Album not found'}), 403


# Route to get Songs of Albums
@app.route('/albums/<int:album_id>/songs', methods=['GET'])
def get_album_songs(album_id):
    album = Album.query.get(album_id)
    if album:
        songs = Song.query.filter_by(album_id=album_id).all()
        serialized_songs = [{
            'id': song.id,
            'name': song.name,
            'lyrics': song.lyrics,
            'genre': song.genre,
            'duration': song.duration,
            'date_created': song.date_created,
            'file_path': song.file_path,
            'added_by': song.user.username
        } for song in songs]
        return jsonify(serialized_songs), 200
    else:
        return jsonify({'message': 'Album not found'}), 404



# Route For Logout
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklisted_tokens.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200



if __name__ == '__main__':
    app.run(debug=True)

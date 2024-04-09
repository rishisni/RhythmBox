from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from models import *
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from werkzeug.security import check_password_hash
from sqlalchemy import or_  
import os


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)

#Configuration for Blackinstis the Token
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
blacklisted_tokens = set()

UPLOAD_FOLDER = 'static/uploads/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Set up the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Route For User and Creator Registration
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


#Route For User and Creator Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username_or_email = data.get('usernameOrEmail')
    password = data.get('password')
    user = User.query.filter(or_(User.username == username_or_email, User.email == username_or_email)).first()
    if user:
        if user.is_admin:
            return jsonify({'message': 'Admin login should be done through a separate form'}), 401
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token,'profile_url' :'/profile'}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404


#Route For Admin Login
@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    username_or_email = data.get('usernameOrEmail')
    password = data.get('password')
    user = User.query.filter(or_(User.username == username_or_email, User.email == username_or_email)).first()
    if user:
        if user.is_admin:
            
            if check_password_hash(user.password, password):
                
                access_token = create_access_token(identity=user.id)
                return jsonify({'access_token': access_token,'profile_url' :'/profile'}), 200
            else:
                return jsonify({'message': 'Invalid username or password'}), 401
        else:
            return jsonify({'message': 'Unauthorized access'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404


#Route to Get User Role
@app.route('/user-role', methods=['GET'])
@jwt_required()  
def get_user_role():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({'is_admin': user.is_admin, 'is_creator': user.is_creator}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


#Route For Profile       
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({'username': user.username, 'email': user.email}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


#Route for Getting User Id
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200


#Function for Blockist Loader
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, decoded_token):
    jti = decoded_token["jti"]
    return jti in blacklisted_tokens


#Route For Logout
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklisted_tokens.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200



def generate_unique_filename(filename):
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    filename_without_extension, extension = os.path.splitext(filename)
    return f"{filename_without_extension}.{current_datetime}{extension}"

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
            new_album = Album(name=name, artist=artist, cover_photo=file_path)
            db.session.add(new_album)
            db.session.commit()
            
            return jsonify({'message': 'Album added successfully'}), 201
        else:
            return jsonify({'message': 'File type not allowed'}), 400
    else:
        return jsonify({'message': 'Unauthorized to add albums'}), 403


# Route For Fetching All Albums
@app.route('/albums', methods=['GET'])
@jwt_required()
def get_albums():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    albums = Album.query.all()
    if albums:
        # Serialize the albums data to JSON format
        serialized_albums = [{'id': album.id, 'name': album.name, 'artist': album.artist, 'cover_photo': album.cover_photo,'song_count':album.song_count} for album in albums]
        return jsonify(serialized_albums), 200
    else:
        return jsonify({'message': 'No albums found'}), 404




if __name__ == '__main__':
    app.run(debug=True)

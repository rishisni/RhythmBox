from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from models import *
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from sqlalchemy import or_  


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
db.init_app(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)




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

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user:
        return jsonify({'username': user.username, 'email': user.email}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200


if __name__ == '__main__':
    app.run(debug=True)

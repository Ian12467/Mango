# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'role')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Mango Image Model
class MangoImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(200))
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Mango Image Schema
class MangoImageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'image_path', 'upload_date')

mango_image_schema = MangoImageSchema()
mango_images_schema = MangoImageSchema(many=True)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    role = request.json['role']
    
    new_user = User(username=username, email=email, password=password, role=role)
    
    db.session.add(new_user)
    db.session.commit()
    
    return user_schema.jsonify(new_user)

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:
        return user_schema.jsonify(user)
    else:
        return jsonify({"message": "Invalid credentials"}), 401
from flask import Flask, jsonify

app = Flask(__name__)

# Define the root route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Mango App API!"})

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from models import db, User, Day, Exercise, Training

app = Flask(__name__)

# Allow CORS requests to this API
CORS(app)

load_dotenv()

#Configuring the SQL db
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET')

db.init_app(app)
jwt = JWTManager(app)


with app.app_context():
    db.create_all()

# 1. endpoint to authenticate users and return JWTs
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(user_name=username).first()

    if user is None or user.user_password !=password:
        return jsonify({"msg": "The email or password are incorrect. Please try again."}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# 2. endpoint to get all days names
@app.route('/days', methods=['GET'])
def get_days():
    days = Day.query.all()
    return jsonify([day.days_name for day in days])
    

# 3. endpoint to get all exercises names
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify([exercise.exercises_name for exercise in exercises])
    

# 4. endpoint to create a training
@app.route('/training', methods=['POST'])
def create_training():
    data = request.get_json()
    day = data['day']
    user = data['user']
    exercise1 = data['exercise1']
    exercise2 = data['exercise2']
    exercise3 = data['exercise3']
    new_training = Training(
        training_day_name=day,
        training_user_name=user,
        training_exercise1=exercise1,
        training_exercise2=exercise2,
        training_exercise3=exercise3
    )
    db.session.add(new_training)
    db.session.commit()
    return jsonify({'message': 'The training has been created.'})


# 5. endpoint to retrieve training data
@app.route('/user/<username>/training', methods=['GET'])
def get_training(username):
    training_data = Training.query.filter_by(training_user_name=username).all()
    return jsonify([{
        'training_day_name': training.training_day_name,
        'training_exercise1': training.training_exercise1,
        'training_exercise2': training.training_exercise2,
        'training_exercise3': training.training_exercise3
    } for training in training_data])


# 6. endpoint to update training data
@app.route('/user/<user>/training', methods=['PUT'])
def update_training(user):
    data = request.get_json()
    day = data['day']
    # user = data['user']
    exercise1 = data['exercise1']
    exercise2 = data['exercise2']
    exercise3 = data['exercise3']
    training = Training.query.filter_by(training_user_name=user, training_day_name=day).first()
    if training:
        training.training_exercise1 = exercise1
        training.training_exercise2 = exercise2
        training.training_exercise3 = exercise3
        db.session.commit()
        return jsonify({'message': 'The training has been updated.'})
    else:
        return jsonify({'message': 'Training not found.'}), 404
    

# 7. endpoint to delete training data
@app.route('/user/<username>/training_delete', methods=['DELETE'])
def delete_training(username):
    training = Training.query.filter_by(training_user_name=username).all()
    if training:
        for training_ex in training:
            db.session.delete(training_ex)
        db.session.commit()
        return jsonify({'message': 'The training data has been deleted.'})
    else:
        return jsonify({'message': 'Training not found.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
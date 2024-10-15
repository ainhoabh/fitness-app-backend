from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_cors import CORS
import os
from dotenv import load_dotenv

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Allow CORS requests to this API
CORS(app)

load_dotenv()

#Configuring the SQL db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET')
jwt = JWTManager(app)

db = SQLAlchemy(app)

DATABASE = 'fitness.sqlite'

def get_db_connection():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row
    return db


# 1. endpoint to authenticate users and return JWTs
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE users_name = ?', (username,)).fetchone()
    conn.close()

    if user is None or user['users_password'] !=password:
        return jsonify({"msg": "The email or password are incorrect. Please try again."}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# 2. endpoint to get all days names
@app.route('/days', methods=['GET'])
def get_days():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT days_name FROM days')
    days = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(days)
    

# 3. endpoint to get all exercises names
@app.route('/exercises', methods=['GET'])
def get_exercises():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT exercises_name FROM exercises')
    exercises = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(exercises)
    

# 4. endpoint to create a training
@app.route('/training', methods=['POST'])
def create_training():
    data = request.get_json()
    print(data)
    day = data['day']
    user = data['user']
    exercise1 = data['exercise1']
    exercise2 = data['exercise2']
    exercise3 = data['exercise3']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO training (training_day_name, training_user_name, training_exercise1, training_exercise2, training_exercise3) VALUES (?, ?, ?, ?, ?)', (day, user, exercise1, exercise2, exercise3))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'The training has been created.'})


# 5. endpoint to retrieve training data
@app.route('/user/<username>/training', methods=['GET'])
def get_training(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT training_day_name, training_exercise1, training_exercise2, training_exercise3 FROM training WHERE training_user_name = ?', (username,))
    training_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(training_data)


# 6. endpoint to update training data
@app.route('/user/<user>/training', methods=['PUT'])
def update_training(user):
    data = request.get_json()
    print(data)
    day = data['day']
    user = data['user']
    exercise1 = data['exercise1']
    exercise2 = data['exercise2']
    exercise3 = data['exercise3']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE training SET training_exercise1 = ?, training_exercise2 = ?, training_exercise3 = ? WHERE training_user_name = ? AND training_day_name = ?', (exercise1, exercise2, exercise3, user, day))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'The training has been updated.'})
    

# 7. endpoint to delete training data
@app.route('/user/<username>/training_delete', methods=['DELETE'])
def delete_training(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM training WHERE training_user_name = ?', (username,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'The training data has been deleted.'})


if __name__ == '__main__':
    app.run(debug=True)
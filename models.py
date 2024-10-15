from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(100), nullable=False)

class Day(db.Model):
    __tablename__ = 'days'
    days_name = db.Column(db.String(100), primary_key=True)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    exercises_name = db.Column(db.String(100), primary_key=True)

class Training(db.Model):
    __tablename__ = 'training'
    training_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    training_day_name = db.Column(db.String(100), db.ForeignKey('days.days_name'))
    training_user_name = db.Column(db.String(100), db.ForeignKey('users.user_name'))
    training_exercise1 = db.Column(db.String(100), db.ForeignKey('exercises.exercises_name'))
    training_exercise2 = db.Column(db.String(100), db.ForeignKey('exercises.exercises_name'))
    training_exercise3 = db.Column(db.String(100), db.ForeignKey('exercises.exercises_name'))

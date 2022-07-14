from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import null

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credits = db.Column(db.Integer, default=10)
    wins = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    loses = db.Column(db.Integer, default=0)
    date_created = db.Column(db.Date, default=date.today())

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    credits = db.Column(db.Integer, nullable=True)
    result = db.Column(db.Integer, nullable=True)
    gametime = db.Column(db.Time, nullable=True)


from game import routes
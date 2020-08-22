from functools import wraps
from flask import Flask, request, render_template, redirect, url_for, flash, session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:a123456@localhost:3306/user?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_COMMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

# 定义ORM
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    def __repr__(self):
        return '<User %r>' % self.username


def create_db():
    db.create_all()

    admin = User(id = 1, username='admin', password='root', email='admin@example.com')
    db.session.add(admin)
    guestes = [User(id = 2,username='guest1', password='a123456', email='guest1@example.com'),
               User(id = 3,username='guest2', password='a123456', email='guest2@example.com'),
               User(id = 4,username='guest3', password='a123456', email='guest3@example.com'),
               User(id = 5,username='guest4', password='a123456', email='guest4@example.com')]
    db.session.add_all(guestes)
    db.session.commit()

create_db()
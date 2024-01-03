from dashlink import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    urls = db.relationship('Url', backref='owner', lazy=True)
    session_id = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}')"


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    long_url = db.Column(db.String(100), nullable=False)
    short_url = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Url('{self.title}', '{self.long_url}', '{self.short_url}', '{self.desc}', {self.date_created})"


# class UserSession(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     session_id = db.Column(db.String(120), unique=True, nullable=False)
#     user = db.relationship('User', backref=db.backref('sessions', lazy=True))
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager
from . import db

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pitch(db.Model):
    '''
    Movie class to define Movie Objects
    '''
    __tablename__ = 'pitch'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    details = db.Column(db.String) 
    votes = db.Column(db.Integer)
    category = db.Column(db.String)
    comments = db.relationship('Comment',backref = 'pitch',lazy = 'dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls,category):
        pitches = Pitch.query.filter_by(category = category).all()
        return pitches

    def __repr__(self):
        return f'Pitch {self.post}'

class Comment(db.Model):
    '''
    Comments class to define comment objects
    '''
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    posted = db.Column(db.Time,default=datetime.utcnow())
    pitch_title = db.Column(db.String(255))
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch_id):
        comments = Comment.query.filter_by(pitch_id=pitch_id).all()
        return comments

    def __repr__(self):
        return f'comment:{self.comment}'

class User(UserMixin,db.Model):
    '''
    Class User defines users as objects
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    comments = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(255))
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
    profile_pic_path = db.Column(db.String())

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

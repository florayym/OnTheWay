from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    tel = db.Column(db.String(11), unique=True, nullable=True)
    sex = db.Column(db.Enum('F', 'M'), server_default='F')
    birth = db.Column(db.Date, nullable=True)
    tags = db.Column(db.String(50), nullable=True)

    comments = db.relationship('Comment', backref='poster', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nickname

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Store(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    storename = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(500), nullable=False)
    longtitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float, default=0)
    special = db.Column(db.Text, nullable=True)
    img_url = db.Column(db.Text, nullable=True)
    word_cloud = db.Column(db.Text, nullable=True)

    comments = db.relationship('Comment', backref='store', lazy='dynamic')

    def __repr__(self):
        return '<Store %r>' % self.storename


class Comment(db.Model):

    __tabelname__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    comment = db.Column(db.Text, nullable=False)
    comment_score = db.Column(db.Float, nullable=False, index=True)
    comment_time = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return '<Comment %r from user %r >' % (self.store_id, self.user_id)






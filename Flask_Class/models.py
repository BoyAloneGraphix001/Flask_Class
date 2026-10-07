from Flask_Class import db, login_manager
from flask import current_app
from datetime import datetime, timezone
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
     return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False )
    email = db.Column(db.String(120), unique = True, nullable = False )
    password = db.Column(db.String(255), nullable = False )
    status = db.Column(db.String(20), default = 'user', nullable = False )
    image_file = db.Column(db.String(21), default = 'default.jpeg', nullable = False )
    posts = db.relationship('Post', backref = 'author', lazy =True)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=max_age)['user_id']
        except:
            return None
        return db.session.get(User, user_id)

    def __repr__(self): 
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False )
    date_posted = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), nullable = False )
    content = db.Column(db.Text, nullable = False )
    description = db.Column(db.String(200), nullable = False )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
            return f"Post('{self.title}', '{self.date_posted}')"
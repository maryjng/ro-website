from datetime import datetime
import hashlib

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = hashlib.md5(password.encode()).hexdigest()
        user = User(username=username, email=email, password=hashed_pwd)

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`. searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            hashed_pw = hashlib.md5(password.encode()).hexdigest()
            if hashed_pw == user.password:
                return user

        return False
    

#table cart_inventory
    #id, char_id

#table char
    #char_id, account_id
    #hair, hair_color, clothes_color, body
    #weapon, shield, head_top, head_mid, head_bottom, robe, 
#table 



######################################

def connect_db(app):
    db.app = app
    db.init_app(app)

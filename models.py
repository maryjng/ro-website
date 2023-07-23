from datetime import datetime
import hashlib

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "login"

    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.VARCHAR(39), nullable=False, unique=True)
    userid = db.Column(db.VARCHAR(23), nullable=False, unique=True)
    user_pass = db.Column(db.VARCHAR(32), nullable=False)

    sex = db.Column(db.Text, nullable=False, default='M')
    group_id = db.Column(db.Integer, nullable=False, default=0)
    state = db.Column(db.Integer, nullable=False, default=0)
    unban_time = db.Column(db.Integer, nullable=False, default=0)
    expiration_time = db.Column(db.Integer, nullable=False, default=0)
    logincount = db.Column(db.Integer, nullable=False, default=0)
    lastlogin = db.Column(db.DateTime)
    last_ip = db.Column(db.VARCHAR(100), nullable=False, default='')
    birthdate = db.Column(db.DateTime)
    character_slots = db.Column(db.Integer, nullable=False, default=0)
    pincode = db.Column(db.VARCHAR(4), nullable=False, default='')
    pincode_change = db.Column(db.Integer, nullable=False, default=0)
    vip_time = db.Column(db.Integer, nullable=False, default=0)
    old_group = db.Column(db.Integer, nullable=False, default=0)
    web_auth_token = db.Column(db.VARCHAR(17))
    web_auth_token_enabled = db.Column(db.Integer, nullable=False, default=0)


    @classmethod
    def signup(cls, userid, email, user_pass):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = hashlib.md5(user_pass.encode()).hexdigest()
        user = User(userid=userid, email=email, user_pass=hashed_pwd)

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, userid, password):
        """Find user with `username` and `password`. searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(userid=userid).first()

        if user:
            hashed_pw = hashlib.md5(password.encode()).hexdigest()
            if hashed_pw == user.user_pass:
                return user

        return False
    
    @classmethod
    def check_no_duplicates(cls, userid):
        #returns True if username doesn't exist already
        user = cls.query.filter_by(userid=userid).first()

        if user:
            return False
        return True
    

#table cart_inventory
    #id, char_id

#table char
    #char_id, account_id
    #hair, hair_color, clothes_color, body
    #weapon, shield, head_top, head_mid, head_bottom, robe, 
#table 



# class Characters(db.Model):
#     __tablename__ = "characters"

#     char_id = db.Column(db.Integer, primary_key=True)
#     account_id = db.Column(db.Integer, nullable=False)
#     hair = db.Column(db.Integer, nullable=False)
#     hair_color = db.Column(db.Integer, nullable=False)
#     clothes_color = db.Column(db.Integer, nullable=False)
#     body = db.Column(db.Integer, nullable=False)
#     weapon = db.Column(db.Integer, nullable=False)
#     shield = db.Column(db.Integer, nullable=False)
#     head_top = db.Column(db.Integer, nullable=False)
#     head_mid = db.Column(db.Integer, nullable=False)
#     head_bottom = db.Column(db.Integer, nullable=False)
#     robe = db.Column(db.Integer, nullable=False)

#     @classmethod
#     def get_all_chars(cls, account_id):

#         chars_res = cls.query((characters.char_id).filter(characters.account_id=account_id).all())
#         chars = {}
#         for 

#table char
    #char_id, account_id
    #hair, hair_color, clothes_color, body
    #weapon, shield, head_top, head_mid, head_bottom, robe, 

######################################

def connect_db(app):
    db.app = app
    db.init_app(app)

import base64
import random
import string
from sqlalchemy import join, exc, and_, select
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, flash, redirect, session, g, url_for, request
# from flask_debugtoolbar import DebugToolbarExtension
from forms import UserAddForm, LoginForm
from models import db, User, connect_db
from captcha.image import ImageCaptcha
import config


CURR_USER_KEY = "curr_user"

image = ImageCaptcha()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/openro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = config.SECRET_KEY

connect_db(app)

#########################################################################
def generate_captcha_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = db.session.query(User).filter_by(userid=session[CURR_USER_KEY])

    else:
        g.user = None


@app.route("/")
@app.route("/home", methods=["GET"])
def index():
    # if g.user:
    #     return redirect(url_for("show_account"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.authenticate(form.username.data,
                                    form.password.data)

            if user:
                session[CURR_USER_KEY] = user.userid

                return redirect(url_for("index"))
            else:
                raise Exception("Authentication failed.")
        
        except:
            flash('Incorrect credentials.')
            return render_template("login.html", form=form)
    
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            captcha_input = request.form.get('captcha_input')
            expected_captcha = session.get("captcha_code")

            if captcha_input != expected_captcha:
                raise ValueError("Captcha input does not match.")

            #Check for matching passwords and if username is taking. Throw errors where needed and handle
            pw_confirm = form.confirm_password.data
            password = form.password.data
            if pw_confirm != password:
                raise ValueError('Passwords do not match.')

            if User.check_no_duplicates(userid=form.username.data):
                user = User.signup(
                userid = form.username.data,
                email = form.email.data,
                user_pass = form.password.data)

                db.session.commit()

                flash("Registration successful.")
                session[CURR_USER_KEY] = user.account_id

                return redirect(url_for("index"))
            
            else:
                raise IntegrityError("Username already in use.")

        except IntegrityError as e:
            print(e)
            flash("Username already taken.", 'danger')

        except ValueError as e:
            print(e)
            flash(e, 'danger')
    
    #generate captcha code, assign to session, and create the image
    captcha_code = generate_captcha_code()
    session["captcha_code"] = captcha_code
    captcha_image = image.generate(captcha_code)
    captcha_image = base64.b64encode(captcha_image.read()).decode()

    return render_template("register.html", form=form, captcha_image=captcha_image,mimetype="image/png")


@app.route("/logout")
def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        return redirect(url_for("index"))

#################################################################################

# @app.route("/account")
# def show_account():
#     if g.user:
#         #query user's chars and their equipment and cloth color from db

#         return render_template("account.html", characters=characters)

#     return redirect(url_for("index"))

###############################################################################

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

import os
# import requests

from sqlalchemy import join, exc, and_
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, flash, redirect, session, g, url_for
# from flask_debugtoolbar import DebugToolbarExtension
from key import API_KEY, SECRET_KEY, USERNAME, PASSWORD

from forms import UserAddForm, LoginForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

engine = sqlalchemy.create_engine(f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}}/{DBNAME}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "SECRET_KEY"

app.debug = True
# toolbar = DebugToolbarExtension(app)

connect_db(app)

#########################################################################

@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route("/")
@app.route("/home", methods=["GET"])
def index():
    # if g.user:
    #     return redirect(url_for("trackings"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.authenticate(form.username.data,
                                    form.password.data)

            if user:
                session[CURR_USER_KEY] = user.id

                return redirect(url_for("index"))
        
        except:
            flash('Incorrect credentials.')
            return render_template("login.html", form=form)
    
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            pw_confirm = form.confirm_password.data
            password = form.password.data
            if pw_confirm != password:
                raise ValueError('Passwords do not match.')

            user = User.signup(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data)

            db.session.commit()

            flash("Registration successful.")
            session[CURR_USER_KEY] = user.id

            return redirect(url_for("index"))

        except IntegrityError as e:
            flash("Username already taken.", 'danger')
            return render_template("register.html", form=form)
        except ValueError as e:
            flash("Passwords must match.", 'danger')
            return render_template("register.html", form=form)

    else:
        return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        return redirect(url_for("index"))

#################################################################################

###############################################################################

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

import unittest
from unittest import TestCase
from flask import session

from models import db, User

from app import app, CURR_USER_KEY


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/testopenro'

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


class HomeViewsTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

            u1 = User.signup(userid="testuser1", email="test1@test.com", user_pass="HASHED_PASSWORD")
            u1id = 1
            u1.id = u1id

            u2 = User.signup(userid="testuser2", email="test2@test.com", user_pass="HASHED_PASSWORD")
            u2id = 2
            u2.id = u2id

            db.session.commit()

            u1 = db.session.get(User, u1id)
            self.u1 = u1
            self.u1_id = u1id

            u2 = db.session.get(User, u2id)
            self.u2 = u2
            self.u2_id = u2id

            self.client = app.test_client()


    def tearDown(self):
        with app.app_context():
            resp=super().tearDown()
            db.session.rollback()
            return resp

    def test_index_anon(self):
        """tests if index page displays correctly when not logged in."""

        with self.client as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Hello</h2>', html)

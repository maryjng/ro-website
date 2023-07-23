from unittest import TestCase
from sqlalchemy import exc
import hashlib

from models import db, User

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/testopenro'


class UserModelTestCase(TestCase):
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

            self.u1 = db.session.query(User).filter_by(userid='testuser1').first()
            self.u1_id = u1id

            self.u2 = db.session.query(User).filter_by(userid='testuser2').first()
            self.u2_id = u2id

            self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            res = super().tearDown()
            db.session.rollback()
            return res

    def test_user_model(self):
        """Does basic model work?"""
        with app.app_context():
            u = User(
                email="test3@test.com",
                userid="testuser3",
                user_pass="HASHED_PASSWORD"
            )

            db.session.add(u)
            db.session.commit()

            query_user = db.session.get(User, 3)

            self.assertEqual(query_user.account_id, 3)
            self.assertEqual(query_user.email, "test3@test.com")
            self.assertEqual(query_user.userid, "testuser3")

    def test_user_signup_valid(self):
        """Does User.signup successfully create new user with valid credentials?"""
        with app.app_context():

            user = User.signup(userid="testuser3", email="test3@test.com", user_pass="HASHED_PASSWORD")
            uid = 3
            db.session.commit()

            test = db.session.get(User, uid)
            self.assertIsNotNone(test)
            self.assertEqual(test.userid, "testuser3")
            self.assertEqual(test.email, "test3@test.com")
            self.assertNotEqual(test.user_pass, "HASHED_PASSWORD")
            # self.assertTrue(test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        with app.app_context():
            invalid = User.signup(None, "test@test.com", "password")
            uid = 123456789
            invalid.id = uid
            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()

    def test_invalid_email_signup(self):
        with app.app_context():
            invalid = User.signup("testtest", None, "password")
            uid = 123789
            invalid.id = uid
            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()

    # def test_invalid_password_signup(self):
    #     with app.app_context():
    #         with self.assertRaises(ValueError) as context:
    #             User.signup("testtest", "email@email.com", "")

    #         with self.assertRaises(ValueError) as context:
    #             User.signup("testtest", "email@email.com", None)


#auth

    def test_valid_authentication(self):
        with app.app_context():
            u = User.authenticate(self.u1.userid, "HASHED_PASSWORD")
            self.assertIsNotNone(u)
            self.assertEqual(u.account_id, self.u1_id)

    def test_invalid_username(self):
        with app.app_context():
            self.assertFalse(User.authenticate("badusername", "HASHED_PASSWORD"))

    def test_wrong_password(self):
        with app.app_context():
            self.assertFalse(User.authenticate(self.u1.userid, "badpassword"))

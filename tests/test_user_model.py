import unittest
from app import create_app, db
from app.models import User, Role, AnonymousUser, Permission


class UserModelTestCase(unittest.TestCase):
    def test_passworld_setter(self):
        u = User(password='zhan')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='zhan')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='zhan')
        self.assertTrue(u.verify_password('zhan'))
        self.assertFalse(u.verify_password('peng'))

    def test_password_salts_are_random(self):
        u = User(password='zhan')
        u2 = User(password='zhan')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='zhanyunpeng1996@qq.com', password='123')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

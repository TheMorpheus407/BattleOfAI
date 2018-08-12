import unittest
import requests
from tests.IAM.UserDTO import userDTO as UserDTO, session


url = "http://0.0.0.0:1338/api/iam/"

def drop_all_add_one():
    session.drop_all()
    session.add(UserDTO("Challo", "somemail@domain.com", "asdf1234", True))
    session.commit()

class RegisterTest(unittest.TestCase):
    def setUp(self):
        drop_all_add_one()

    def test_new_user(self):
        username = "HalloWelt"
        email = "somemail@domain.com"
        data = {
  "username": username,
  "email": email,
  "password": "asdf1234",
  "newsletter": True
}
        resp = requests.post(url + "register", json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["success"], True)
        user = UserDTO.query.filter_by(username="HalloWelt").first()
        self.assertFalse(user is None)
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password("asdf1234"), True)
        self.assertEqual(user.newsletter, True)
        self.assertEqual(user.email_verified, False)
        self.assertFalse(user.email_token is None)
        self.assertTrue(user.token is None)
        self.assertTrue(user.session_token is None)

    def test_add_existing_user(self):
        username = "Challo"
        email = "somemail@domain.com"
        data = {
            "username": username,
            "email": email,
            "password": "asdf1234",
            "newsletter": True
        }
        resp = requests.post(url + "register", json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["success"], False)


class VerifyEmailTest(unittest.TestCase):
    def setUp(self):
        drop_all_add_one()

    def test_verify_mail(self):
        user = UserDTO.query.filter_by(username="Challo").first()
        self.assertFalse(user is None)
        resp = requests.post(url + "verifyEmail", json={"email_token": user.email_token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["success"], True)
        user = UserDTO.query.filter_by(id=user.id).first()
        self.assertTrue(user.is_verified())
        self.assertTrue(user.email_token is None)


class VerifyVerifiedEmailTest(unittest.TestCase):
    def setUp(self):
        drop_all_add_one()
        user = UserDTO.query.filter_by(username="Challo").first()
        self.assertFalse(user is None)
        resp = requests.post(url + "verifyEmail", json={"email_token": user.email_token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["success"], True)

    def test_verify_mail(self):
        user = UserDTO.query.filter_by(username="Challo").first()
        self.assertFalse(user is None)
        self.assertTrue(user.is_verified())
        resp = requests.post(url + "verifyEmail", json={"email_token": user.email_token})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["success"], False)

if __name__ == '__main__':
    unittest.main()

import unittest
from flask_testing import TestCase
from app import app, db, User

class TestUsersEndpoint(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_users(self):
        response = self.client.get('/airline/users')
        self.assertEqual(response.status_code, 200)
        expected_result = [
            {"id": 1, "username": "user1", "email": "user1@example.com"},
            {"id": 2, "username": "user2", "email": "user2@example.com"}
        ]
        self.assertEqual(response.json, expected_result)

    def test_create_user(self):
        new_user_data = {
            "username": "new_user", "email": "new_user@example.com"}
        response = self.client.post('/airline/users/create', json=new_user_data)
        self.assertEqual(response.status_code, 200)
        created_user = User.query.filter_by(
            email="new_user@example.com").first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "new_user")

    def test_get_one_user(self):
        response = self.client.get('/airline/users/user1@example.com')
        self.assertEqual(response.status_code, 200)
        expected_result = {
            "id": 1, "username": "user1", "email": "user1@example.com"}
        self.assertEqual(response.json, expected_result)

    def test_update_one_user(self):
        update_data = {
            "username": "updated_user", "email": "user1@example.com"}
        response = self.client.put('/airline/users/update/user1@example.com', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_user = User.query.filter_by(email="user1@example.com").first()
        self.assertEqual(updated_user.username, "updated_user")

    def test_delete_one_user(self):
        response = self.client.delete(
            '/airline/users/delete/user1@example.com')
        self.assertEqual(response.status_code, 200)
        deleted_user = User.query.filter_by(email="user1@example.com").first()
        self.assertIsNone(deleted_user)


if __name__ == '__main__':
    unittest.main()

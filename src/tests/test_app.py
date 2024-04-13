import unittest
from flask_testing import TestCase
from app import app, db, User

class TestUsersEndpoint(TestCase):
    def create_app(self):
        """
        Create and configure the Flask app instance.
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        """
        Set up the test environment by creating necessary database tables, adding users 
        for testing, and committing the changes.
        """
        db.create_all()
        user1 = User(username="user1", email="user1@example.com")
        user2 = User(username="user2", email="user2@example.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        """
        Tear down method to remove the session and drop all tables in the database.
        """
        db.session.remove()
        db.drop_all()

    def test_get_all_users(self):
        """
        Test for getting all users via the API endpoint '/airline/users'.
        Asserts that the response status code is 200 and the JSON response matches the expected result.
        """
        response = self.client.get('/airline/users')
        self.assertEqual(response.status_code, 200)
        expected_result = [
            {"id": 1, "username": "user1", "email": "user1@example.com"},
            {"id": 2, "username": "user2", "email": "user2@example.com"}
        ]
        self.assertEqual(response.json, expected_result)

    def test_create_user(self):
        """
        Test creating a new user by sending a POST request with new user data. 
        Asserts that the response status code is 200, checks if the user was created 
        in the database, and validates the created user's username.
        """
        new_user_data = {
            "username": "new_user", "email": "new_user@example.com"}
        response = self.client.post('/airline/users/create', json=new_user_data)
        self.assertEqual(response.status_code, 200)
        created_user = User.query.filter_by(
            email="new_user@example.com").first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.username, "new_user")

    def test_get_one_user(self):
        """
        A test case to get one user using the client and assert the response and expected result.
        """
        response = self.client.get('/airline/users/user1@example.com')
        self.assertEqual(response.status_code, 200)
        expected_result = {
            "id": 1, "username": "user1", "email": "user1@example.com"}
        self.assertEqual(response.json, expected_result)

    def test_update_one_user(self):
        """
        A test case to update a single user's information.
        """
        update_data = {
            "username": "updated_user", "email": "user1@example.com"}
        response = self.client.put('/airline/users/update/user1@example.com', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_user = User.query.filter_by(email="user1@example.com").first()
        self.assertEqual(updated_user.username, "updated_user")

    def test_delete_one_user(self):
        """
        Test for deleting one user.
        """
        response = self.client.delete(
            '/airline/users/delete/user1@example.com')
        self.assertEqual(response.status_code, 200)
        deleted_user = User.query.filter_by(email="user1@example.com").first()
        self.assertIsNone(deleted_user)


if __name__ == '__main__':
    unittest.main()

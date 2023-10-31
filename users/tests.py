from rest_framework.test import APITestCase
from users.models import User


class TestUser(APITestCase):
    def test_create_user(self):
        new_username = "testuser"
        new_password = "123"

        response = self.client.post(
            "/api/v1/users/",
            data={
                "username": new_username,
                "password": new_password,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            response.data["username"],
            new_username,
        )

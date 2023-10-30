from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestProjectEditor(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_project(self):
        new_project_title = "Test Project"
        new_project_photo = "https://i.imgur.com/M1F6LC4.png"
        new_project_description = "this is test project"
        new_project_category = "stationery"

        response = self.client.post(
            "/api/v1/projects/project-editor",
            data={
                "title": new_project_title,
                "photo": new_project_photo,
                "description": new_project_description,
                "category": new_project_category,
            },
        )

        self.assertEqual(
            response.status_code,
            403,
        )
        self.client.force_login(
            self.user,
        )

        response = self.client.post(
            "/api/v1/projects/project-editor",
            data={
                "title": new_project_title,
                "photo": new_project_photo,
                "description": new_project_description,
                "category": new_project_category,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            response.data["title"],
            new_project_title,
        )

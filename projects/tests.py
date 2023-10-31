from rest_framework.test import APITestCase
from . import models
from users.models import User
from categories.models import Category


class TestProjectEditor(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user = user

        category = Category.objects.create(pk=1)
        category.save()
        self.category = category

    def test_create_project(self):
        new_project_title = "Test Project"
        new_project_photo_url = "https://i.imgur.com/M1F6LC4.png"
        new_project_description = "this is test project"

        response = self.client.post(
            "/api/v1/projects/project-editor",
            data={
                "title": new_project_title,
                "photo_url": new_project_photo_url,
                "description": new_project_description,
                "category": self.category.pk,
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
                "photo": new_project_photo_url,
                "description": new_project_description,
                "category": self.category.pk,
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


class TestProjectEditorDetail(APITestCase):
    def setUp(self):
        user = User.objects.create(username="test")
        user.set_password("123")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.user = user

        category = Category.objects.create(pk=1)
        category.save()
        self.category = category

        self.new_project_title = "Test Project"
        self.new_project_photo = "https://i.imgur.com/M1F6LC4.png"
        self.new_project_description = "this is test project"

        new_project = models.Project(
            title=self.new_project_title,
            photo=self.new_project_photo,
            description=self.new_project_description,
            category=self.category,
            user=self.user,
        )
        new_project.save()

    def test_project_not_found(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.get("/api/v1/projects/project-editor/2")

        self.assertEqual(response.status_code, 404)

    def test_get_project(self):
        self.client.force_login(
            self.user,
        )

        response = self.client.get("/api/v1/projects/project-editor/1")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["title"],
            self.new_project_title,
        )

    def test_patch_project(self):
        self.client.force_login(
            self.user,
        )
        response = self.client.patch(
            "/api/v1/projects/project-editor/1",
            data={"is_approved": "approval"},
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        self.assertEqual(
            data["is_approved"],
            "approval",
        )

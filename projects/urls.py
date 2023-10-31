from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProjectList.as_view()),
    path("project-editor", views.ProjectEditor.as_view()),
    path("project-editor/<int:pk>", views.ProjectEditorDetail.as_view()),
    path("uploads", views.S3Uploads.as_view()),
]

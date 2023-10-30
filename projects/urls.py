from django.urls import path
from . import views

urlpatterns = [
    path("project-editor", views.ProjectEditor.as_view()),
    path("project-editor/<int:pk>", views.ProjectEditorDetail.as_view()),
]

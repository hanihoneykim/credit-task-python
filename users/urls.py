from django.urls import path
from . import views

urlpatterns = [
    path("@<str:username>", views.PublicUser.as_view()),
    path("me/projects", views.MyProjects.as_view()),
]

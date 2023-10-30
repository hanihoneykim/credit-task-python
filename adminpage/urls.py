from django.urls import path
from . import views


urlpatterns = [
    path("", views.AdminPage.as_view()),
    path("under-review", views.UnderReview.as_view()),
]

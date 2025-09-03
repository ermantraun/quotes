from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_quote, name="add_quote"),
    path("top/", views.top_quotes, name="top_quotes"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("like/<int:pk>/", views.like_quote, name="like_quote"),
]
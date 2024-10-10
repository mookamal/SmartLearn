from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("<str:slug>/", views.show_category, name="show_category"),
]

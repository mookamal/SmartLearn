from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/", views.profile, name="profile"),
    path("<str:username>/set_interest", views.set_interest, name="set_interest"),
]

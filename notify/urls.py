from django.urls import path
from .views import read_all_notify

urlpatterns = [
    path("ajax/read-all-notify/", read_all_notify, name="read_all_notify"),
]

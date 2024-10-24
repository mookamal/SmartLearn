from django.urls import path
from .views import read_all_notify, notify_list

urlpatterns = [
    path("notify_list/", notify_list, name="notify_list"),
    # ajax
    path("ajax/read-all-notify/", read_all_notify, name="read_all_notify"),
]

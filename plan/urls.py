from django.urls import path
from . import views
urlpatterns = [
    path("payments", views.payment_view, name="payment_view"),
    path("ajax/payment", views.payment, name="payment"),
]

from django.urls import path
from . import views
urlpatterns = [
    path("payments", views.payment_view, name="payment_view"),
    path("payment_details", views.payment_details, name="payment_details"),
    # ajax
    path("ajax/payment", views.payment, name="payment"),
    path("ajax/apply-referral/", views.apply_referral, name="apply_referral")
]

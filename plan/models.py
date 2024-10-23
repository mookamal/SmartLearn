from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.utils import timezone
SUBSCRIPTION_PLAN_CHOICES = [
    ('FREE', 'Free Plan'),
    ('BASIC', 'Basic Plan'),
    ('PREMIUM', 'Premium Plan'),
]


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, choices=SUBSCRIPTION_PLAN_CHOICES)
    sessions_per_month = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # Monthly price
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.get_name_display()


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.OneToOneField(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now_add=True)
    sessions_used = models.IntegerField(default=0)
    last_reset = models.DateField(default=timezone.now)

    @property
    def end_date(self):
        return self.start_date + timedelta(days=30)

    def reset_sessions(self):
        if date.today().day == 1:
            self.sessions_used = 0
            self.last_reset = timezone.now()
            self.save()

    def can_use_session(self):
        return self.sessions_used < self.plan.sessions_per_month

    def use_session(self):
        if self.can_use_session():
            self.sessions_used += 1
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username}'s Subscription"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        UserSubscription, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    approved = models.BooleanField()
    status = models.CharField(max_length=50)
    auth_code = models.CharField(max_length=20)
    reference = models.CharField(max_length=100)
    last4 = models.CharField(max_length=4)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    issuer = models.CharField(max_length=100)
    processed_on = models.DateTimeField()
    expires_on = models.DateTimeField()
    acquirer_transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.reference} - {self.amount} {self.currency}"

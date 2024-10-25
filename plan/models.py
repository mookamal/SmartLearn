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
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sessions_used = models.IntegerField(default=0)
    last_reset = models.DateField(default=timezone.now)
    active_paid_plan = models.BooleanField(default=False)

    def renew_subscription(self):
        self.start_date = timezone.now().date()
        self.end_date = timezone.now().date() + timedelta(days=30)
        self.active_paid_plan = True
        self.sessions_used = 0
        self.save()

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
    payment_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    approved = models.BooleanField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    auth_code = models.CharField(max_length=20, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    last4 = models.CharField(max_length=4, blank=True, null=True)
    expiry_month = models.IntegerField(blank=True, null=True)
    expiry_year = models.IntegerField(blank=True, null=True)
    issuer = models.CharField(max_length=100, blank=True, null=True)
    processed_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.reference} - {self.amount} {self.currency}"


class ReferralCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sessions_for_referrer = models.PositiveIntegerField(default=30)
    sessions_for_referred = models.PositiveIntegerField(default=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class ReferredUser(models.Model):
    referral_code = models.ForeignKey(
        ReferralCode, related_name='referred_users', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} referred by {self.referral_code.code}"

import random
import string
from .models import ReferralCode, UserSubscription
from django.utils import timezone
from datetime import timedelta


def get_subscriptions_expiring_in_3_days():
    target_date = timezone.now().date() + timedelta(days=3)
    expiring_subscriptions = UserSubscription.objects.filter(
        active_paid_plan=True,
        end_date=target_date
    )

    return expiring_subscriptions


def get_all_user_subscriptions_expiring_today():
    target_date = timezone.now().date()
    expiring_subscriptions = UserSubscription.objects.filter(
        active_paid_plan=True,
        end_date=target_date
    )

    return expiring_subscriptions


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def create_referral_code(user):
    code = generate_referral_code()
    ReferralCode.objects.create(code=code, user=user)

from .models import UserSubscription
from django.utils import timezone
from datetime import timedelta


def get_subscriptions_expiring_in_3_days():
    target_date = timezone.now().date() + timedelta(days=3)
    expiring_subscriptions = UserSubscription.objects.filter(
        active_paid_plan=True,
        end_date=target_date
    )

    return expiring_subscriptions

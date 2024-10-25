from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from plan.models import SubscriptionPlan, UserSubscription
from plan.utility import create_referral_code


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        free_plan = SubscriptionPlan.objects.get(name='FREE')
        UserSubscription.objects.create(user=instance, plan=free_plan)
        create_referral_code(instance)
    instance.profile.save()

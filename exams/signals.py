from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Category
from django.template.defaultfilters import slugify
from .models import Session
from django.contrib import messages


@receiver(pre_save, sender=Category)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(post_save, sender=Session)
def check_user_subscription(sender, instance, created, **kwargs):
    if created:
        user_subscription = instance.user.usersubscription
        total_count = user_subscription.plan.sessions_per_month + \
            user_subscription.free_sessions
        if user_subscription.sessions_used < total_count:
            user_subscription.sessions_used += 1
            user_subscription.save()

        else:
            instance.delete()
            messages.error(
                instance.user, "You have reached the maximum number of sessions for this month.")

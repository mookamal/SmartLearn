from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Category
from django.template.defaultfilters import slugify


@receiver(pre_save, sender=Category)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

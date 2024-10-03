from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, default="", blank=True)
    primary_interest = models.ForeignKey('PrimaryInterest',
                                         on_delete=models.SET_NULL, null=True, blank=True,
                                         limit_choices_to={'children__isnull': True})

    def __str__(self):
        return f"{self.user.username}'s Profile"


class PrimaryInterest(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="children",
                               limit_choices_to={'parent__isnull': True})
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name

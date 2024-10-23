from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.template.defaultfilters import slugify
# Create your models here.


class Info(models.Model):
    USD = 'USD'
    SAR = 'SAR'

    CURRENCY_CHOICES = [
        (USD, 'US Dollar'),
        (SAR, 'Saudi Riyal'),
    ]
    name = models.CharField(max_length=200, blank=True, null=True)
    desc = models.TextField()
    logo = models.ImageField(upload_to='logo', default='logo.png')
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default=USD)
    # social media links
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        if Info.objects.exists():
            raise Exception('Only one instance of Info model is allowed.')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

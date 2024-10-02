from django.db import models

# Create your models here.


class Info(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    desc = models.TextField()
    logo = models.ImageField(upload_to='logo', default='logo.png')
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

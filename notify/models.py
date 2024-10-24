from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Notify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    @classmethod
    def mark_all_as_read(self, user):
        self.objects.filter(user=user, is_read=False).update(is_read=True)

    def __str__(self):
        return self.notification

    class Meta:
        ordering = ['-created_at']

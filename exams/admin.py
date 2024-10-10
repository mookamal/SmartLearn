from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Exam)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Category)
admin.site.register(models.Session)
admin.site.register(models.Revision)
admin.site.register(models.Issue)
admin.site.register(models.Choice)

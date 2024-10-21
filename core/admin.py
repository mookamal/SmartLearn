from django.contrib import admin
from .models import Info, Page
# Register your models here.
info_name = Info.objects.first().name if Info.objects.exists() else "Info"

admin.site.register(Page)
admin.site.register(Info)
admin.site.site_header = info_name
admin.site.site_title = info_name

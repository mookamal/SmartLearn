from django.contrib import admin
from .models import Info, Page
from django.core.cache import cache
# Register your models here.

site_name = "Admin Ask Pro"


admin.site.register(Page)
admin.site.register(Info)
admin.site.site_header = site_name
admin.site.site_title = site_name

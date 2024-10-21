from django.contrib import admin
from . import models
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'middle_name',
                    'last_name', 'nickname', 'primary_interest')
    search_fields = ('user__username', 'first_name', 'last_name')


admin.site.register(models.Profile, ProfileAdmin)


class PrimaryInterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('parent',)


admin.site.register(models.PrimaryInterest, PrimaryInterestAdmin)

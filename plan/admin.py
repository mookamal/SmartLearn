from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription
# Register your models here.


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'sessions_per_month', 'price')
    list_filter = ('name',)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'sessions_used')


admin.site.register(UserSubscription, UserSubscriptionAdmin)

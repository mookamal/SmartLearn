from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Payment
# Register your models here.


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'sessions_per_month', 'price')
    list_filter = ('name',)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'sessions_used')


admin.site.register(UserSubscription, UserSubscriptionAdmin)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'timestamp')
    list_filter = ('subscription', 'timestamp')
    search_fields = ('subscription',
                     'subscription__user__email')

from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Payment, ReferralCode, ReferredUser
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
    list_display = ('subscription', 'amount', 'currency', 'status')
    list_filter = ('subscription', 'currency', 'status')
    search_fields = ('subscription',
                     'subscription__user__email')


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'user__email')


@admin.register(ReferredUser)
class ReferredUserAdmin(admin.ModelAdmin):
    list_display = ('referral_code', 'user', 'created_at')

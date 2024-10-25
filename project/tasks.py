from celery import shared_task
from plan.models import UserSubscription, SubscriptionPlan
from notify.models import Notify
from plan.utility import get_subscriptions_expiring_in_3_days, get_all_user_subscriptions_expiring_today
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def reset_free_plan_sessions():
    logger.info("Starting reset_free_plan_sessions task")
    subscriptions = UserSubscription.objects.filter(plan__name='FREE')
    for subscription in subscriptions:
        subscription.reset_sessions()
        # send notification to user about expiring subscription
        Notify.objects.create(
            user=subscription.user,
            notification=f"Your subscription to {
                subscription.plan.name} is expiring in 3 days."
        )
    logger.info("Finished reset_free_plan_sessions task")
    return True


@shared_task
def send_notification_to_users_about_expiring_subscriptions():
    logger.info(
        "Starting send_notification_to_users_about_expiring_subscriptions task")
    subscriptions_expiring_in_3_days = get_subscriptions_expiring_in_3_days()
    for subscription in subscriptions_expiring_in_3_days:
        # send notification to user about expiring subscription
        Notify.objects.create(
            user=subscription.user,
            notification=f"Your subscription to {
                subscription.plan.name} is expiring in 3 days."
        )
    logger.info(
        "Finished send_notification_to_users_about_expiring_subscriptions task")
    return True

# get ending plan and convent plan to free plan


@shared_task
def convent_plan_to_free_plan():
    logger.info("Starting convent_plan_to_free_plan task")
    subscriptions_expiring_today = get_all_user_subscriptions_expiring_today()
    get_free_plan = SubscriptionPlan.objects.filter(name="FREE").first()
    for subscription in subscriptions_expiring_today:
        subscription.plan = get_free_plan
        subscription.active_paid_plan = False
        subscription.sessions_used = 0
        subscription.save()
        # send notification to user about expiring subscription
        Notify.objects.create(
            user=subscription.user,
            notification=f"Your subscription to {
                subscription.plan.name} has been converted to FREE."
        )
    logger.info("Finished convent_plan_to_free_plan task")
    return True

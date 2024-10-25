from celery import shared_task
from plan.models import UserSubscription
from notify.models import Notify
from plan.utility import get_subscriptions_expiring_in_3_days
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

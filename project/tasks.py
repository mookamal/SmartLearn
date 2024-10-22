from celery import shared_task
from plan.models import UserSubscription
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def reset_free_plan_sessions():
    logger.info("Starting reset_free_plan_sessions task")
    subscriptions = UserSubscription.objects.filter(plan__name='FREE')
    for subscription in subscriptions:
        subscription.reset_sessions()
    logger.info("Finished reset_free_plan_sessions task")
    return True

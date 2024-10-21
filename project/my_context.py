import logging
from django.core.cache import cache
from core.models import Info, Page
from plan.models import SubscriptionPlan
from exams.models import Category
logger = logging.getLogger(__name__)


def my_context(request):
    try:
        info = cache.get('info')
        pages = cache.get('pages')
        parent_categories = cache.get('parent_category')
        subscription_plans = cache.get('plans')

        if not info:
            info = Info.objects.first()
            cache.set('info', info, timeout=60*15)

        if not pages:
            pages = Page.objects.order_by('id')[:4]
            cache.set('pages', pages, timeout=60*15)

        if not parent_categories:
            parent_categories = Category.objects.filter(
                parent_category__isnull=True, is_listed=True).order_by('id')
            cache.set('parent_categories', parent_categories, timeout=60*15)

        if not subscription_plans:
            subscription_plans = SubscriptionPlan.objects.all()
            cache.set('plans', subscription_plans, timeout=60*15)

        return {
            'info': info,
            'pages': pages,
            'parent_categories': parent_categories,
            'plans': subscription_plans
        }

    except Info.DoesNotExist:
        logger.warning("No Info object found")
        return {}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {}
    except Page.DoesNotExist:
        logger.warning("No Page object found")
        return {}
    except Category.DoesNotExist:
        logger.warning("No Category object found")
        return {}
    except SubscriptionPlan.DoesNotExist:
        logger.warning("No SubscriptionPlan object found")
        return {}

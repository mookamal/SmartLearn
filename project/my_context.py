import logging
from django.core.cache import cache
from core.models import Info, Page
from exams.models import Category
logger = logging.getLogger(__name__)


def my_context(request):
    try:
        info = cache.get('info')
        pages = cache.get('pages')
        parent_categories = cache.get('parent_category')

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

        return {
            'info': info,
            'pages': pages,
            'parent_categories': parent_categories
        }

    except Info.DoesNotExist:
        logger.warning("No Info object found")
        return {}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {}

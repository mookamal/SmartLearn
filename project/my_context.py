from core.models import Info
from core.models import Page


def my_context(request):
    try:
        info = Info.objects.first()
        pages = Page.objects.all()[:4]
        return {'info': info, 'pages': pages}
    except Info.DoesNotExist:
        return {}

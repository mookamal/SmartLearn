from core.models import Info


def my_context(request):
    try:
        info = Info.objects.first()
        return {'info': info}
    except Info.DoesNotExist:
        return {}

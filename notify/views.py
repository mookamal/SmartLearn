from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import Notify
# Create your views here.

# views


@login_required
def notify_list(request):
    notifications = Notify.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'notify/notify_list.html', {'notification_all': notifications})

# ajax actions


@login_required
@require_GET
def read_all_notify(request):
    Notify.mark_all_as_read(request.user)
    return JsonResponse({"success": True})

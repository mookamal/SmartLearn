from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import Notify
# Create your views here.

# ajax actions


@login_required
@require_GET
def read_all_notify(request):
    Notify.mark_all_as_read(request.user)
    return JsonResponse({"success": True})

from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Create your views here.


@login_required
def payment_view(request):
    return render(request, 'plan/payment_view.html')

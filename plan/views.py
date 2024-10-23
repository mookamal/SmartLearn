from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import SubscriptionPlan, Payment
import json
from django.contrib import messages
from django.http import JsonResponse
from .payment_method import process_payment
# Create your views here.


@login_required
def payment_view(request):
    return render(request, 'plan/payment_view.html')


# for ajax


@require_POST
@login_required
def payment(request):
    card_expiration = request.POST.get('card-expiration')
    # data
    full_name = request.POST.get('full_name')
    card_number = request.POST.get('card-number')
    expiry_year = card_expiration.split("/")[1]
    expiry_month = card_expiration.split("/")[0]
    cvv = request.POST.get('cvv')
    currency = request.POST.get('currency')
    plan = request.POST.get('plans')
    plan_obj = get_object_or_404(SubscriptionPlan, id=int(plan))
    amount = int(plan_obj.price)
    response = process_payment(amount=amount, currency=currency,
                               expiry_year=expiry_year, expiry_month=expiry_month, card_number=card_number, cvv=cvv)
    print("response", response)
    return JsonResponse({"success": True})

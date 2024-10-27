from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import SubscriptionPlan, Payment
from django.contrib import messages
from django.http import JsonResponse
from .payment_method import process_payment
import requests
from notify.models import Notify
from .utility import apply_referral_code
# Create your views here.


@login_required
def payment_view(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'plan/payment_view.html', {'payments': payments})


@login_required
def payment_details(request):
    return render(request, 'plan/payment_details.html')

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
    if not all([full_name, card_number, expiry_month, expiry_year, cvv, currency, plan]):
        return JsonResponse({"error": "Please fill all fields."}, status=400)
    # Get the new plan
    new_plan_obj = get_object_or_404(SubscriptionPlan, id=int(plan))
    amount = int(new_plan_obj.price)

    # Get the current user and their subscription
    current_user = request.user
    user_subscription = current_user.usersubscription

    # Create a Payment object
    payment_obj = Payment(subscription=user_subscription, user=current_user)

    # Process the payment
    try:
        response = process_payment(
            amount=amount,
            currency=currency,
            expiry_year=expiry_year,
            expiry_month=expiry_month,
            card_number=card_number,
            cvv=cvv
        )
        status_code = response.status_code
        response = response.json()
        # Check if payment was approved and authorized
        if status_code == 201:
            # set data from response to payment object
            payment_obj.payment_id = response.get('id')
            payment_obj.amount = amount
            payment_obj.currency = currency
            payment_obj.approved = response.get('approved')
            payment_obj.status = response.get('status')
            payment_obj.auth_code = response.get('auth_code')
            payment_obj.reference = response.get('reference')
            payment_obj.last4 = response.get('source')['last4']
            payment_obj.expiry_month = expiry_month
            payment_obj.expiry_year = expiry_year
            payment_obj.issuer = response.get('source')['issuer']
            payment_obj.processed_on = response.get('processed_on')
            if response.get('approved'):
                if response.get('status') in ["Captured", "Authorized"]:
                    # Update the user's subscription
                    user_subscription.plan = new_plan_obj
                    user_subscription.save()
                    payment_obj.save()
                    # renew date in user_subscription
                    user_subscription.renew_subscription()
                    # cerate DJ message success
                    messages.success(request, "Payment Successful")
                    # create Notify
                    notify = Notify(
                        user=current_user,
                        notification=f"Your payment for {
                            new_plan_obj.name} plan was successful.",
                    )
                    notify.save()
                    return JsonResponse({"success": "Payment Successful"})
            else:
                payment_obj.save()
                # create Notify with
                notify = Notify(
                    user=current_user,
                    notification=f"Payment failed. {
                        response['response_summary']}",
                )
                notify.save()
                return JsonResponse({"error": response['response_summary']}, status=400)

    except requests.exceptions.RequestException as e:
        # Log the error and notify the user
        return JsonResponse({"error": f"Payment service error: {str(e)}"}, status=500)


@require_POST
@login_required
def apply_referral(request):
    referral_code = request.POST.get('referral_code')
    if not referral_code:
        return JsonResponse({"error": "Please provide a referral code."}, status=400)
    # Apply the referral code
    applied = apply_referral_code(request.user, referral_code)
    if applied:
        return JsonResponse({"success": "Referral code applied successfully."})
    else:
        return JsonResponse({"error": "Invalid or expired referral code."}, status=400)

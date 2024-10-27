from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.lib.pagesizes import A4
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
import random
import string
from .models import ReferralCode, UserSubscription, ReferredUser
from django.utils import timezone
from datetime import timedelta
from notify.models import Notify


def get_subscriptions_expiring_in_3_days():
    target_date = timezone.now().date() + timedelta(days=3)
    expiring_subscriptions = UserSubscription.objects.filter(
        active_paid_plan=True,
        end_date=target_date
    )

    return expiring_subscriptions


def get_all_user_subscriptions_expiring_today():
    target_date = timezone.now().date()
    expiring_subscriptions = UserSubscription.objects.filter(
        active_paid_plan=True,
        end_date=target_date
    )

    return expiring_subscriptions


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def create_referral_code(user):
    code = generate_referral_code()
    ReferralCode.objects.create(code=code, user=user)


def apply_referral_code(user, code):
    try:
        referral_code = ReferralCode.objects.get(code=code, is_active=True)

        if referral_code.user == user:
            return False

        if not ReferredUser.objects.filter(referral_code=referral_code, user=user).exists():
            user_subscription_referral = UserSubscription.objects.get(
                user=referral_code.user)
            user_subscription_referral.free_sessions += referral_code.sessions_for_referrer
            user_subscription_referral.save()
            # create notify to referral_code.user
            Notify.objects.create(
                user=referral_code.user,
                notification=f"Your friend {
                    user.username} has referred you for free sessions.",
            )
            # get user_subscription for current user
            user_subscription = UserSubscription.objects.get(user=user)
            user_subscription.free_sessions += referral_code.sessions_for_referred
            user_subscription.save()
            # create notify to user
            Notify.objects.create(
                user=user,
                notification=f"You have earned free sessions for referring {
                    referral_code.user.username}.",
            )
            ReferredUser.objects.create(referral_code=referral_code, user=user)

            return True
    except ReferralCode.DoesNotExist:
        return False


def generate_invoice_pdf(payment):
    buffer = ContentFile(b"")
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.drawString(100, 750, f"Amount : {payment.amount}")
    pdf.drawString(100, 700, f"Plan name : {payment.plan}")
    processed_on = payment.processed_on
    if isinstance(processed_on, str):
        processed_on = datetime.fromisoformat(processed_on[:-1])

    pdf.drawString(100, 650, f"Processed on : {
                   processed_on.strftime('%d-%m-%Y %H:%M:%S')}")
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer


def send_invoice_email(email, payment):
    pdf_buffer = generate_invoice_pdf(payment)
    subject = f"Invoice for {payment.currency} {payment.plan}"
    message = f"Your invoice for {
        payment.plan} has been generated. Please find it attached."
    email = EmailMessage(
        subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    email.attach("invoice.pdf", pdf_buffer.read(), "application/pdf")
    email.send()

def check_subscription(request) -> bool:
    user_subscription = request.user.usersubscription
    if user_subscription.sessions_used < user_subscription.plan.sessions_per_month:
        return True

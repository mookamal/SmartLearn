from django.contrib.auth.models import User
from exams.models import Answer


def check_subscription(request) -> bool:
    user_subscription = request.user.usersubscription
    if user_subscription.sessions_used < user_subscription.plan.sessions_per_month:
        return True


def get_user_answer_statistics(user):

    correct_answers = Answer.objects.filter(
        session__user=user, is_correct=True).count()
    incorrect_answers = Answer.objects.filter(
        session__user=user, is_correct=False).count()

    total_answers = correct_answers + incorrect_answers
    if total_answers == 0:
        return {"correct_rate": 0, "incorrect_rate": 0}

    correct_rate = round((correct_answers / total_answers) * 100)
    incorrect_rate = round((incorrect_answers / total_answers) * 100)

    return {
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "total_answers": total_answers,
        "correct_rate": correct_rate,
        "incorrect_rate": incorrect_rate
    }

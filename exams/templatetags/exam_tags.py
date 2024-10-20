from django import template
from exams.models import Exam, Source, Subject, Question, Session, Answer

register = template.Library()


@register.filter(name='question_count_by_source')
def question_count_by_source(exam_id, source_id):
    try:
        exam = Exam.objects.get(id=exam_id)
        source = Source.objects.get(id=source_id)
        questions_count = exam.get_questions().filter(sources=source).count()
        return questions_count
    except (Exam.DoesNotExist, Source.DoesNotExist):
        return 0


@register.filter(name='question_count_by_subject')
def question_count_by_subject(exam_id, subject_id):
    try:
        exam = Exam.objects.get(id=exam_id)
        subject = Subject.objects.get(id=subject_id)
        questions_count = exam.get_questions().filter(subject=subject).count()
        return questions_count
    except (Exam.DoesNotExist, Subject.DoesNotExist):
        return 0


@register.filter(name="question_status")
def question_status(session_id, question_id):
    try:
        session = Session.objects.filter(id=session_id).first()
        question = Question.objects.filter(id=question_id).first()

        if not session or not question:
            return "not found"

        answer = Answer.objects.filter(
            question=question, session=session).first()

        if answer:
            return '<i class="fa-solid fa-square-check text-green-400"></i>' if answer.is_correct else '<i class="fa-solid fa-square-xmark text-red-400"></i>'
        else:
            return '<i class="fa-solid fa-circle-question text-yellow-200"></i>'

    except Exception as e:
        return str(e)


@register.filter(name="percentage_question")
def percentage_question(question_id):
    try:
        question = Question.objects.filter(id=question_id).first()
        if not question:
            return 0

        answers = Answer.objects.filter(question=question)
        total_count = answers.count()

        if total_count == 0:
            return 0

        correct_count = answers.filter(is_correct=True).count()

        return round((correct_count / total_count) * 100)

    except Question.DoesNotExist:
        return 0
    except Answer.DoesNotExist:
        return 0
    except Exception as e:
        return f"Error: {str(e)}"


@register.simple_tag
def percentage_session_questions(session, result):
    total_questions = session.questions.count()
    if result == "correct":
        return round((session.correct_answer_count / total_questions) * 100)
    elif result == "incorrect":
        return round((session.incorrect_answer_count / total_questions) * 100)
    elif result == "skipped":
        return round((session.skipped_answer_count / total_questions) * 100)


@register.simple_tag
def user_questions_answered_in_exam(exam, user, target):
    all_pks = Answer.objects.filter(
        question__exam=exam, session__user=user).values('question')

    q = Question.objects.filter(exam=exam)
    total_count = q.filter(pk__in=all_pks).count()

    if total_count == 0:
        return 0 if target == "total" else {"correct": 0, "incorrect": 0, "skipped": 0}

    if target == "total":
        return total_count

    correct_count = q.filter(pk__in=all_pks, answer__choice__is_right=True,
                             answer__session__user=user).distinct().count()
    incorrect_count = q.filter(pk__in=all_pks, answer__choice__is_right=False,
                               answer__session__user=user).distinct().count()
    skipped_count = q.filter(pk__in=all_pks, answer__choice__is_right__isnull=True,
                             answer__session__user=user).distinct().count()

    if target == "percent":
        return {
            "correct": round((correct_count / total_count) * 100),
            "incorrect": round((incorrect_count / total_count) * 100),
            "skipped": round((skipped_count / total_count) * 100),
        }

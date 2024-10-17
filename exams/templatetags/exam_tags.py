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

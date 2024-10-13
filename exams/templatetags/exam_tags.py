from django import template
from exams.models import Exam, Source, Subject

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

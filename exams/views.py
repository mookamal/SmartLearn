import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Category, Exam, Session
from django.http import JsonResponse
# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'exams/dashboard.html')


@login_required
def show_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {'category': category}
    return render(request, 'exams/show_category.html', context)


@login_required
def show_exams_by_category(request, slug, sub_category_id):
    category = get_object_or_404(
        Category.objects.select_related('parent_category'),
        pk=sub_category_id,
        parent_category__slug=slug
    )

    exams = category.exams.filter(is_visible=True)

    context = {
        'exams': exams,
        'category': category
    }

    return render(request, 'exams/show_exams_by_category.html', context)


@login_required
def create_session(request, slug, sub_category_id, exam_id):
    category = get_object_or_404(
        Category.objects.select_related('parent_category'),
        pk=sub_category_id,
        parent_category__slug=slug
    )
    exam = get_object_or_404(
        Exam, pk=exam_id, category=category, is_visible=True)
    context = {
        'exam': exam,
        'category': category
    }
    return render(request, 'exams/create_session.html', context)

# functions for ajax


@login_required
@require_POST
def get_question_count(request):
    data = json.loads(request.body)

    subjects = data.get('subjects', None)
    sources = data.get('sources', None)
    exam_id = data.get('exam_id', None)

    exam = get_object_or_404(Exam, id=exam_id)

    questions = exam.get_questions().prefetch_related('subject', 'sources')

    if subjects and subjects != ['all']:
        questions = questions.filter(subject__id__in=subjects)

    if sources and sources != ['all']:
        questions = questions.filter(sources__id__in=sources)
    question_count = questions.count()

    return JsonResponse({'question_count': question_count})


@login_required
@require_POST
def ajax_create_session(request):
    try:
        data = json.loads(request.body)
        current_user = request.user
        subjects = data.get('subjects', None)
        sources = data.get('sources', None)
        exam_id = data.get('exam_id', None)
        session_mode = data.get('sessionFeel', None)
        num_questions = int(data.get('numQuestions', 0))

        if num_questions <= 0:
            return JsonResponse({'error': 'Invalid number of questions'}, status=400)

        exam = get_object_or_404(Exam, id=exam_id)

        questions = exam.get_questions().prefetch_related('subject', 'sources')

        if subjects and 'all' not in subjects:
            questions = questions.filter(subject__id__in=subjects)

        if sources and 'all' not in sources:
            questions = questions.filter(sources__id__in=sources)

        questions = questions.order_by('?')[:num_questions]

        session = Session.objects.create(
            user=current_user, exam=exam, session_mode=session_mode)

        session.questions.add(*questions)

        return JsonResponse({'session_id': session.id})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)

import json
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Category, Exam, Session, Question, Choice, Answer
from django.http import JsonResponse
from django.contrib import messages
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


@login_required
def show_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, user=request.user)
    question_order = session.question_order
    current_index = session.current_question_index
    # if current_index >= len(question_order):
    #     session.completed = True
    #     session.save()
    #     return render(request, 'exams/session_complete.html')
    current_question_id = question_order[current_index]
    current_question = get_object_or_404(Question, id=current_question_id)
    try:
        answer = Answer.objects.filter(
            session=session, question=current_question).first()
    except Answer.DoesNotExist:
        answer = None
    choices = Choice.objects.filter(question=current_question)
    percentage = (current_index / len(question_order)) * 100

    # this for show question solved
    should_display = session.session_mode == 'SOLVED' or (
        answer is not None) and session.session_mode != 'UNEXPLAINED'
    context = {
        'session': session,
        'question': current_question,
        'current_index': current_index,
        'total_questions': len(question_order),
        "percentage": percentage,
        'choices': choices,
        'answer': answer,
        'should_display': should_display,
    }
    return render(request, 'exams/show_session.html', context)


# functions for ajax


@ login_required
@ require_POST
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


@ login_required
@ require_POST
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
        question_ids = list(questions.values_list('id', flat=True))

        session = Session.objects.create(
            user=current_user, exam=exam, session_mode=session_mode, number_of_questions=num_questions, question_order=question_ids)

        session.questions.add(*questions)

        messages.success(
            request, f'Session created successfully. Session ID: #{session.id}')

        return JsonResponse({'session_id': session.id})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)


@ login_required
@ require_POST
def answer(request):
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', None)
        question_id = data.get('question_id', None)
        choice_id = data.get('choice_id', None)
        session = get_object_or_404(Session, id=session_id, user=request.user)
        question = get_object_or_404(Question, id=question_id)
        choice = get_object_or_404(Choice, id=choice_id)
        answer = Answer.objects.create(
            session=session, question=question, choice=choice)

        return JsonResponse({'answer_id': answer.id})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Session.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
    except Choice.DoesNotExist:
        return JsonResponse({'error': 'Choice not found'}, status=404)


@ login_required
@ require_POST
def navigate_question_index(request):
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', None)
        action = data.get('action', None)
        session = get_object_or_404(Session, id=session_id, user=request.user)
        if action == 'next':
            if session.current_question_index < len(session.question_order) - 1:
                session.current_question_index += 1
        elif action == 'prev':
            if session.current_question_index > 0:
                session.current_question_index -= 1

        session.save()
        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Session.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

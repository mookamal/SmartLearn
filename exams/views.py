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
    total_questions = len(question_order)
    last_index = total_questions - 1
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
        'total_questions': total_questions,
        "percentage": percentage,
        'choices': choices,
        'answer': answer,
        'should_display': should_display,
        "last_index": last_index,
    }
    return render(request, 'exams/show_session.html', context)


@login_required
def session_results(request, session_id):
    session = get_object_or_404(Session, id=session_id, user=request.user)
    total_questions = session.number_of_questions
    if total_questions > 0:
        percentage_correct_answer = round(
            session.correct_answer_count / total_questions * 100)
        percentage_incorrect_answer = round(
            session.incorrect_answer_count / total_questions * 100)
        percentage_skipped_answer = round(
            session.skipped_answer_count / total_questions * 100)
    context = {
        'percentage_correct_answer': percentage_correct_answer,
        'percentage_incorrect_answer': percentage_incorrect_answer,
        'percentage_skipped_answer': percentage_skipped_answer,
        'session': session,
    }
    # return template
    return render(request, 'exams/session_results.html', context)


@login_required
def my_sessions(request):
    sessions = Session.objects.filter(user=request.user)
    context = {'sessions': sessions}
    return render(request, "exams/my_sessions.html", context)

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
            user=current_user, exam=exam, session_mode=session_mode, number_of_questions=num_questions)

        session.questions.add(*questions)
        session.question_order = list(
            session.questions.values_list('id', flat=True))
        session.unused_question_count = questions.count()
        session.update_answer_counts()
        messages.success(
            request, f'Session created successfully. Session ID: #{session.id}')
        return JsonResponse({'session_id': session.id})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_POST
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
        if session.unused_question_count > 0:
            session.unused_question_count -= 1
        session.save()
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


@login_required
@require_POST
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
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)


@login_required
@require_POST
def finish_session(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id", None)
        session = get_object_or_404(Session, id=session_id, user=request.user)
        session.unused_question_count = 0
        session.update_answer_counts()
        session.mark_as_completed()
        return JsonResponse({"success": True})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Session.DoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)


@login_required
@require_POST
def re_examine(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id", None)
        action = data.get("action", None)

        if not session_id or not action:
            return JsonResponse({"error": "Invalid action or session_id"}, status=400)

        if action not in ["all", "skipped", "incorrect"]:
            return JsonResponse({"error": "Invalid action"}, status=400)

        session = get_object_or_404(Session, id=session_id, user=request.user)

        if action == "all":
            questions = session.questions.all()
        elif action == "skipped":
            questions = session.questions.filter(
                answer__isnull=True, session=session)
        elif action == "incorrect":
            questions = session.questions.filter(
                answer__choice__is_right=False, session=session)

        if not questions.exists():
            return JsonResponse({"error": "No questions found for the specified action"}, status=404)

        # create a new session
        new_session = Session.objects.create(
            user=session.user,
            exam=session.exam,
            session_mode=session.session_mode,
            number_of_questions=questions.count(),
            question_order=list(questions.values_list('id', flat=True)),
            current_question_index=0,
        )
        # add all questions to the new session
        new_session.questions.add(*questions)
        # update answer counts for the new session
        new_session.update_answer_counts()
        return JsonResponse({"session_id": new_session.id})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Session.DoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)


@login_required
@require_POST
def delete_session(request):
    try:
        data = json.loads(request.body)
        action = data.get("action", None)
        session_id = data.get("session_id", None)

        if action == "all":
            Session.objects.filter(user=request.user).delete()
            messages.success(request, "All sessions deleted successfully.")
        elif action == "single" and session_id:
            session = get_object_or_404(
                Session, id=session_id, user=request.user)
            session.delete()
            messages.success(request, "Session deleted successfully.")
        else:
            return JsonResponse({"error": "Invalid action or missing session_id"}, status=400)

        return JsonResponse({"success": True})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Session.DoesNotExist:
        return JsonResponse({"error": "Session not found"}, status=404)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

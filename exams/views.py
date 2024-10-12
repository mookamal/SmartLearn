from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Category, Exam
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
    exam = get_object_or_404(Exam, pk=exam_id, category=category)
    context = {
        'exam': exam,
        'category': category
    }
    return render(request, 'exams/create_session.html', context)

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Category
# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'exams/dashboard.html')


@login_required
def show_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {'category': category}
    return render(request, 'exams/show_category.html', context)

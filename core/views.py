from django.shortcuts import render
from .models import Page
from django.shortcuts import get_object_or_404
# Create your views here.


def home(request):
    pages = Page.objects.all()[:4]
    return render(request, 'core/home.html', {'pages': pages})


def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'core/page.html', {'page': page})

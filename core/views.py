from django.shortcuts import render
from .models import Page
# Create your views here.


def home(request):
    pages = Page.objects.all()[:4]
    return render(request, 'core/home.html', {'pages': pages})

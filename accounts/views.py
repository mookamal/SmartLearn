from django.shortcuts import render
from .models import Profile
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
# Create your views here.


def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.user != profile.user:
        return HttpResponseForbidden("You don't have permission to view this profile.")
    return render(request, 'accounts/profile.html', {'profile': profile})

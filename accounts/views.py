from django.shortcuts import render, redirect
from .models import Profile, PrimaryInterest
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .forms import ProfileForm
from django.contrib import messages
# Create your views here.


def profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    if request.user != profile.user:
        return HttpResponseForbidden("You don't have permission to view this profile.")
    form = ProfileForm(instance=profile)
    primary_interests = PrimaryInterest.objects.all()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', username=username)
    context = {'profile': profile, 'form': form,
               "primary_interests": primary_interests}
    return render(request, 'accounts/profile.html', context)


def set_interest(request, username):
    if request.method == 'POST':
        interest_id = request.POST.get("secondary_interest")
        if request.user.username == username:
            profile = get_object_or_404(Profile, user__username=username)
            if interest_id:
                interest = get_object_or_404(PrimaryInterest, id=interest_id)
                profile.primary_interest = interest
                profile.save()
                messages.success(request, 'Interest updated successfully.')
                return redirect('profile', username=request.user.username)

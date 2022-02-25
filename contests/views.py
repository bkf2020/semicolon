from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Contest, Registration
from .forms import RegisterForm

# Create your views here.

def home(request):
    contests = Contest.objects.all()
    for contest in contests:
        contest.registered = False

        user_registration = Registration.objects.filter(
            user_id=request.user.id,
            contest_id=contest.id
        )
        if(len(user_registration) > 0):
            contest.registered = True

    context = {
        'contests': reversed(contests)
    }
    return render(request, 'contests/home.html', context)

def register(request, index):
    contest = Contest.objects.get(pk=index)
    registered = False
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            agreed = form.cleaned_data.get('agree')

            if(agreed):
                new_user_registration = Registration(
                    user_id=request.user.id,
                    contest_id = contest.id
                )
                new_user_registration.save()
                messages.success(request, f"You have registered for {contest.name}!")
                return redirect('contests-home')

    else:
        form = RegisterForm()

    user_registration = Registration.objects.filter(
        user_id=request.user.id,
        contest_id=index
    )
    if(len(user_registration) > 0):
        registered = True

    context = {
        'contest': contest,
        'form': form,
        'registered': registered
    }
    return render(request, 'contests/register.html', context)

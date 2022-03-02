from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Contest, ContestProblem, Registration
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

        if timezone.now() > contest.end_time:
            contest.ended = True
        elif timezone.now() >= contest.start_time:
            contest.started = True
            messages.info(request, f"{contest.name} is in progress!")

    context = {
        'contests': reversed(contests)
    }
    return render(request, 'contests/home.html', context)

def register(request, index):
    contest = Contest.objects.get(pk=index)
    registered = False

    if timezone.now() >= contest.start_time:
        messages.error(request, f"Registration has closed for {contest.name}.")
        return redirect('contests-home')

    if not request.user.is_authenticated:
        messages.error(request, "Please log in before registering for the contest!")
        return redirect(f'/login/?next={request.path}')
    
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

def arena(request, index):
    contest = Contest.objects.get(pk=index)
    user_registration = Registration.objects.filter(
        user_id=request.user.id,
        contest_id=index
    )
    contest_problems = ContestProblem.objects.filter(
        contest=contest
    )
    
    if timezone.now() < contest.start_time:
        messages.error(request, f"{contest.name} hasn't started yet!")
        return redirect('contests-home')
    elif timezone.now() <= contest.end_time:
        contest.running = True
        if not request.user.is_authenticated:
            messages.error(request, f"Please login before taking {contest.name}! Note you must be registered on your account!")
            return redirect(f'/login/?next={request.path}')
        elif len(user_registration) == 0:
            messages.error(request, f"You can't take {contest.name} because you haven't registered!")
            return redirect('contests-home')

    context = {
        'contest': contest,
        'contest_problems': contest_problems
    }
    return render(request, 'contests/arena.html', context)

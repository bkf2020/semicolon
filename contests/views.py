from django.shortcuts import render
from django.http import HttpResponse
from .models import Contest, Registration

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

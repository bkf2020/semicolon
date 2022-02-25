from django.shortcuts import render
from django.http import HttpResponse
from .models import Contest

# Create your views here.

def home(request):
    contests = Contest.objects.all()
    context = {
        'contests': reversed(contests)
    }
    return render(request, 'contests/home.html', context)

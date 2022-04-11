from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')



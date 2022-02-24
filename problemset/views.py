from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Problem, Submission
from .forms import ProblemForm

def home(request):
    context = {
        'problemset': reversed(Problem.objects.all())
    }
    return render(request, 'problemset/home.html', context)

def problem(request, index):
    problem = Problem.objects.get(pk=index)
    user_submissions = Submission.objects.filter(
        user_id=request.user.id,
        problem_id=index
    )

    if(not problem.visible and not request.user.is_superuser):
        return render(request, 'problemset/blocked.html')

    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data.get('answer')
            problem_solved = (user_answer == problem.correct_answer)

            if(problem_solved):
                messages.success(request, f"You answer {user_answer} is correct!")
            else:
                messages.error(request, f"You answer {user_answer} is wrong!")

            if(len(user_submissions) == 0):
                new_user_submission = Submission(
                    user_id=request.user.id,
                    problem_id=index,
                    problem_solved=problem_solved
                )
                new_user_submission.save()
            elif(problem_solved):
                current_user_submission = user_submissions[0]
                current_user_submission.problem_solved = True
                current_user_submission.save()

        return redirect('/problemset/' + str(index) + '/')

    else:
        form = ProblemForm()
    
    problem_solved = len(user_submissions) >= 1 and user_submissions[0].problem_solved
    context = {
        'problem': problem,
        'form': form,
        'problem_solved': problem_solved
    }
    return render(request, 'problemset/problem.html', context)

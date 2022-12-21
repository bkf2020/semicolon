import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Contest, ContestProblem, Registration
from .forms import RegisterForm, ProblemForm, MultipleChoiceForm
import math
from problemset.models import Submission

# Create your views here.

def home(request):
    contests = Contest.objects.all().order_by('-id')
    visible_contests = []
    for contest in contests:
        contest.joined = False

        user_registration = Registration.objects.filter(
            user_id=request.user.id,
            contest_id=contest.id
        )
        if(len(user_registration) > 0):
            contest.joined = True
            time_diff = datetime.timedelta(minutes=contest.time_limit)
            contest.user_end_time = user_registration[0].time_joined + time_diff
            if contest.user_end_time > contest.end_time:
                contest.user_end_time = contest.end_time
            if timezone.now() <= contest.user_end_time:
                contest.running = True

        if timezone.now() > contest.end_time:
            contest.ended = True
        elif timezone.now() >= contest.start_time:
            contest.started = True
            messages.info(request, f"{contest.name} is in progress!")

        if(contest.visible):
            visible_contests.append(contest)

    paginator = Paginator(visible_contests, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'current_server_time': math.floor(timezone.now().timestamp())
    }
    return render(request, 'contests/home.html', context)

def confirm(request, index):
    contest = Contest.objects.get(pk=index)

    if timezone.now() > contest.end_time:
        messages.error(request, f"You cannot take {contest.name} officially anymore.")
        return redirect('contests-home')

    if not request.user.is_authenticated:
        messages.error(request, "Please log in before joining the contest!")
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
                messages.success(request, f"You have joined {contest.name}!")
                return redirect(f'/contests/{index}/semiarena/')

    else:
        form = RegisterForm()

    user_registration = Registration.objects.filter(
        user_id=request.user.id,
        contest_id=index
    )
    if(len(user_registration) > 0):
        messages.success(request, f"You already have joined this contest!")
        return redirect(f'/contests/{index}/semiarena/')

    context = {
        'contest': contest,
        'form': form,
        'current_server_time': math.floor(timezone.now().timestamp())
    }
    return render(request, 'contests/confirm.html', context)

def semiarena(request, index):
    contest = Contest.objects.get(pk=index)
    user_registration = Registration.objects.filter(
        user_id=request.user.id,
        contest_id=index
    )
    contest_problems = ContestProblem.objects.filter(
        contest=contest
    ).order_by('id')

    if request.method == 'POST':
        form = ProblemForm(request.POST)
        redirect_url = '/contests/' + str(index) + '/semiarena/'
        if form.is_valid():
            problem_id = int(form.cleaned_data.get('problem_id'))
            problem = contest_problems[problem_id].problem
            user_answer = form.cleaned_data.get('answer')
            redirect_url += '#' + str(problem_id + 1)

            user_submissions = Submission.objects.filter(
                user_id=request.user.id,
                problem_id=problem.id
            )
            problem_solved = (user_answer == problem.correct_answer)
            
            contest_running = False
            time_diff = datetime.timedelta(minutes=contest.time_limit)
            if(len(user_registration) > 0):
                user_end_time = user_registration[0].time_joined + time_diff
                if user_end_time > contest.end_time:
                    user_end_time = contest.end_time
                if timezone.now() <= user_end_time:
                    contest_running = True

            submissions_remaining = 5
            if(contest_running and len(user_submissions) > 0):
                submissions_remaining = 5 - user_submissions[0].wrong_submissions_in_contest

            if(submissions_remaining == 0):
                pass
            elif(problem_solved):
                messages.success(request, f"Your answer {user_answer} for problem {problem_id + 1} is correct!")
            else:
                if(contest_running):
                    messages.error(request, f"Your answer {user_answer} for problem {problem_id + 1} is wrong! You have {submissions_remaining - 1} submissions left.")
                else:
                    messages.error(request, f"Your answer {user_answer} for problem {problem_id + 1} is wrong!")
            
            penalty_diff = 0
            time_solved_in_contest = 0
            wrong_submissions_diff = 0
            solved_in_contest = False
            if(contest_running):
                if(len(user_submissions) > 0 and user_submissions[0].wrong_submissions_in_contest == 5):
                    problem_solved = False
                    messages.error(request, f"You have already made 5 submissions to {problem_id + 1} and cannot make anymore!")
                elif(problem_solved):
                    solved_in_contest = True
                    time_since_start = timezone.now() - user_registration[0].time_joined
                    penalty_diff = int(math.floor(time_since_start.seconds / 60))
                    time_solved_in_contest = int(math.floor(time_since_start.seconds / 60))
                    prev_penalty = 0
                    if(len(user_submissions) > 0):
                        prev_penalty = user_submissions[0].penalty
                    user_registration[0].total_penalty += prev_penalty + penalty_diff
                    user_registration[0].total_points += contest_problems[problem_id].value
                    user_registration[0].save()
                else:
                    penalty_diff = 10 # 10 point penalty for every wrong submission
                    wrong_submissions_diff = 1

            if(len(user_submissions) == 0):
                new_user_submission = Submission(
                    user_id=request.user.id,
                    problem_id=problem.id,
                    problem_solved=problem_solved,
                    solved_in_contest=solved_in_contest,
                    penalty=penalty_diff,
                    time_solved_in_contest=time_solved_in_contest,
                    wrong_submissions_in_contest=wrong_submissions_diff
                )
                new_user_submission.save()
            else:
                current_user_submission = user_submissions[0]
                current_user_submission.problem_solved |= problem_solved
                current_user_submission.solved_in_contest |= solved_in_contest
                current_user_submission.penalty += penalty_diff
                current_user_submission.time_solved_in_contest = time_solved_in_contest
                current_user_submission.wrong_submissions_in_contest += wrong_submissions_diff
                current_user_submission.save()

        return redirect(redirect_url)
    else:
        idx = 0
        for problem in contest_problems:
            problem.form = ProblemForm(initial={'problem_id': idx})
            idx += 1
    
    if timezone.now() < contest.start_time:
        messages.error(request, f"{contest.name} hasn't started yet!")
        return redirect('contests-home')
    elif timezone.now() <= contest.end_time:
        if not request.user.is_authenticated:
            messages.error(request, f"Please login before taking {contest.name}! Note you must have started this contest on your account!")
            return redirect(f'/login/?next={request.path}')
        elif len(user_registration) == 0:
            messages.error(request, f"You can't take {contest.name} because you haven't joined! Please confirm before joining!")
            return redirect(f'/contests/{index}/confirm')
        else:
            time_diff = datetime.timedelta(minutes=contest.time_limit)
            contest.user_end_time = user_registration[0].time_joined + time_diff
            if contest.user_end_time > contest.end_time:
                contest.user_end_time = contest.end_time
            
            if timezone.now() <= contest.user_end_time:
                contest.running = True
            else:
                contest.user_finished_but_running = True
                messages.info(request, "Your attempt for the contest has finished. You can view and submit the problems unofficially. \
                Make sure to follow the rules regarding discussion!")
    else:
        messages.info(request, "The contest is over, but you can view and submit the problems unofficially.")
        contest.ended_for_all = True


    for problem in contest_problems:
        user_submissions = Submission.objects.filter(
            user_id=request.user.id,
            problem_id=problem.problem.id
        )
        problem.solved = len(user_submissions) > 0 and user_submissions[0].problem_solved

    context = {
        'contest': contest,
        'contest_problems': contest_problems,
        'current_server_time': math.floor(timezone.now().timestamp())
    }
    return render(request, 'contests/semiarena.html', context)

def arena(request, index):
    contest = Contest.objects.get(pk=index)
    user_registration = Registration.objects.filter(
        user_id=request.user.id,
        contest_id=index
    )
    contest_problems = ContestProblem.objects.filter(
        contest=contest
    ).order_by('id')

    if timezone.now() < contest.start_time:
        messages.error(request, f"{contest.name} hasn't started yet!")
        return redirect('contests-home')
    elif timezone.now() <= contest.end_time:
        if not request.user.is_authenticated:
            messages.error(request, f"Please login before taking {contest.name}! Note you must have started this contest on your account!")
            return redirect(f'/login/?next={request.path}')
        elif len(user_registration) == 0:
            messages.error(request, f"You can't take {contest.name} because you haven't joined! Please confirm before joining!")
            return redirect(f'/contests/{index}/confirm')
        else:
            time_diff = datetime.timedelta(minutes=contest.time_limit)
            contest.user_end_time = user_registration[0].time_joined + time_diff
            if contest.user_end_time > contest.end_time:
                contest.user_end_time = contest.end_time
            
            if timezone.now() <= contest.user_end_time:
                contest.running = True
            else:
                contest.user_finished_but_running = True
                messages.info(request, "Your attempt for the contest has finished. You can view the problems and submit after the contest \
                ends for everyone. Make sure to follow the rules regarding discussion!")
    else:
        messages.info(request, "The contest is over, but you can view and submit the problems unofficially.")
        contest.ended_for_all = True
    
    if request.method == 'POST':
        if(contest.running):
            if(contest.contest_format == 'AIME'):
                form = ProblemForm(request.POST)
            else:
                form = MultipleChoiceForm(request.POST)

            if form.is_valid():
                problem_id = int(form.cleaned_data.get('problem_id'))
                problem = contest_problems[problem_id].problem
                user_answer = form.cleaned_data.get('answer')
                user_submissions = Submission.objects.filter(
                    user_id=request.user.id,
                    problem_id=problem.id
                )
                if(len(user_submissions) == 0):
                    if(contest.contest_format == 'AIME'):
                        new_user_submission = Submission(
                            user_id=request.user.id,
                            problem_id=problem.id,
                            answer_in_contest=user_answer,
                            solved_in_contest=True
                        )
                        new_user_submission.save()
                    else:
                        new_user_submission = Submission(
                            user_id=request.user.id,
                            problem_id=problem.id,
                            answer_choice_in_contest=user_answer
                        )
                        new_user_submission.save()
                else:
                    if(contest.contest_format == 'AIME'):
                        user_submissions[0].solved_in_contest = True
                        user_submissions[0].answer_in_contest = user_answer
                        user_submissions[0].save()
                    else:
                        user_submissions[0].answer_choice_in_contest = user_answer
                        user_submissions[0].save()
        return JsonResponse(status=200, data={})

    idx = 0
    for problem in contest_problems:
        if(problem.problem.multiple_choice):
            problem.form = MultipleChoiceForm(auto_id=str(idx) + '_%s', initial={'problem_id': idx, 'answer': 'Blank'})
            user_submissions = Submission.objects.filter(
                user_id=request.user.id,
                problem_id=problem.problem.id
            )
            if(len(user_submissions) == 0):
                new_user_submission = Submission(
                    user_id=request.user.id,
                    problem_id=problem.problem.id,
                )
                new_user_submission.save()
        else:
            problem.form = ProblemForm(initial={'problem_id': idx})
        idx += 1
    
    context = {
        'contest': contest,
        'contest_problems': contest_problems,
        'current_server_time': math.floor(timezone.now().timestamp())
    }
    return render(request, 'contests/arena.html', context)

def scoreboard(request, index):
    contest = Contest.objects.get(pk=index)
    contest_problems = ContestProblem.objects.filter(
        contest=contest
    ).order_by('id')
    user_registrations = Registration.objects.filter(
        contest_id=contest.id
    ).order_by('-total_points', 'total_penalty')

    if(timezone.now() <= contest.end_time):
        messages.error(request, f"You cannot view the scoreboard because the contest '{contest.name}' has not finished yet!")
        return redirect('contests-home')
    
    current_rank = 1
    first = True
    prev_score = 0
    prev_penalty = 0
    current_user_rank = 0

    for user in user_registrations:
        if first:
            prev_score = user.total_points
            prev_penalty = user.total_penalty
            first = False
        elif user.total_points < prev_score or user.total_penalty > prev_penalty:
            prev_score = user.total_points
            prev_penalty = user.total_penalty
            current_rank += 1
        user.rank = current_rank
        if(user.user_id == request.user.id):
            current_user_rank = current_rank

        possible_users = User.objects.filter(pk=user.user_id)
        if len(possible_users) > 0:
            user.username = possible_users[0].username
        else:
            user.username = "N/A"

        user_problem_info = []
        for contest_problem in contest_problems:
            user_submissions = Submission.objects.filter(
                user_id=user.user_id,
                problem_id=contest_problem.problem.id
            )
            if len(user_submissions) > 0:
                user_submissions[0].value = contest_problem.value
                user_problem_info.append(user_submissions[0])
            else:
                user_problem_info.append(False)
        
        user.problem_info = user_problem_info
    
    total_num_ranks = current_rank

    paginator = Paginator(user_registrations, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'contest': contest,
        'contest_problems': contest_problems,
        'page_obj': page_obj,
        'current_user_rank': current_user_rank,
        'total_num_ranks': total_num_ranks
    }
    return render(request, 'contests/scoreboard.html', context)

def preview(request, index):
    contest = Contest.objects.get(pk=index)
    contest_problems = ContestProblem.objects.filter(
        contest=contest
    ).order_by('id')
    context = {
        'contest': contest,
        'contest_problems': contest_problems
    }
    if not request.user.is_superuser:
        return redirect('contests-home')
    return render(request, 'contests/preview.html', context)

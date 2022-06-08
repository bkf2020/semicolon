# gives all users free points for one problem and removes
# penalty for this problem
import django
from django.conf import settings
import os
import sys

sys.path.insert(0, '../../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'semicolon_src.settings')
django.setup()

from problemset.models import Problem, Submission
from contests.models import Contest, ContestProblem, Registration

contest_id = int(input("Enter contest id: "))
problem_id = int(input("Enter problem id: "))

problem = Problem.objects.get(id=problem_id)
contest = Contest.objects.get(id=contest_id)

check = input(f"Changing contest {contest.name} and problem {problem.name}. "
               "Are you sure? Type 'YES' (without the quotes)")

if(check != "YES"):
    quit()

contest_problem = ContestProblem.objects.filter(
    contest=contest,
    problem=problem
)
problem_points = 0
if(contest_problem.count() > 0):
    problem_points = contest_problem[0].value

affected_registrations = Registration.objects.filter(
    contest_id=contest_id
)
for registration in affected_registrations:
    user_id = registration.user_id
    submissions = Submission.objects.filter(
        user_id=user_id,
        problem_id=problem_id
    )
    if(len(submissions) > 0):
        if(submissions[0].solved_in_contest):
            registration.total_penalty -= submissions[0].penalty
            registration.save()
        else:
            registration.total_points += problem_points
            registration.save()

        submissions[0].penalty = 0
        submissions[0].time_solved_in_contest = 0
        submissions[0].wrong_submissions_in_contest = 0
        submissions[0].problem_solved = True
        submissions[0].solved_in_contest = True
        submissions[0].save()

    elif(len(submissions) == 0):
        new_submission = Submission(
            user_id=user_id,
            problem_id=problem_id,
            problem_solved=True,
            solved_in_contest=True,
            penalty=0,
            time_solved_in_contest=0,
            wrong_submissions_in_contest=0
        )
        new_submission.save()
        registration.total_points += problem_points
        registration.save()

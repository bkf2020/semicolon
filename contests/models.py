from django.db import models
from django.utils import timezone
from problemset.models import Problem

CONTEST_FORMATS = (
    ('AMC8', 'AMC8'),
    ('AMC10', 'AMC10'),
    ('AIME', 'AIME'),
    ('Semicolon', 'Semicolon')
)

class Contest(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=False)
    start_time_url = models.URLField(default="")
    end_time_url = models.URLField(default="")
    announcement_link = models.URLField(default="")
    time_limit = models.IntegerField(default=0)
    has_solutions = models.BooleanField(default=False)
    solutions_url = models.URLField(default="")
    contest_format = models.CharField(max_length=9, choices=CONTEST_FORMATS, default='Semicolon')
    form_user_submit_solutions = models.BooleanField(default=False)
    form_link = models.URLField(default="")
    
    def __str__(self):
        return self.name

class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f"Contest: {self.contest.name}, Problem: {self.problem.name}"

class Registration(models.Model):
    user_id = models.IntegerField()
    contest_id = models.IntegerField()
    time_joined = models.DateTimeField(default=timezone.now)
    total_points = models.DecimalField(default=0, max_digits=10, decimal_places=1)
    total_penalty = models.IntegerField(default=0)
    confirmed_honest = models.BooleanField(default=False)
    verify_end_time = models.DateTimeField(default=timezone.now)


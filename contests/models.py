from django.db import models
from django.utils import timezone
from problemset.models import Problem

class Contest(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=False)
    start_time_url = models.URLField(default="")
    end_time_url = models.URLField(default="")
    announcement_link = models.URLField(default="")
    time_limit = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Contest: {self.contest.name}, Problem: {self.problem.name}"

class Registration(models.Model):
    user_id = models.IntegerField()
    contest_id = models.IntegerField()
    time_joined = models.DateTimeField(default=timezone.now)
    total_points = models.IntegerField(default=0)
    total_penalty = models.IntegerField(default=0)


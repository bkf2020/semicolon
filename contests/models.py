from django.db import models
from django.utils import timezone
from problemset.models import Problem

class Contest(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class ContestProblem(models.Model):
    contest = models.OneToOneField(Contest, on_delete=models.CASCADE)
    problem = models.OneToOneField(Problem, on_delete=models.CASCADE)

class Registration(models.Model):
    user_id = models.IntegerField()
    contest_id = models.IntegerField()

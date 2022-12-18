from django.db import models
from django.utils import timezone

ANSWER_CHOICES = (
    ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('Blank', 'Blank'),
)

class Problem(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    visible = models.BooleanField(default=False)
    multiple_choice = models.BooleanField(default=True)
    correct_answer = models.IntegerField(default=0)
    correct_answer_choice = models.CharField(max_length=5, choices=ANSWER_CHOICES, default='A')
    def __str__(self):
        return self.name

class Submission(models.Model):
    user_id = models.IntegerField(default=0)
    problem_id = models.IntegerField(default=0)
    problem_solved = models.BooleanField(default=False)
    solved_in_contest = models.BooleanField(default=False)
    penalty = models.IntegerField(default=0)
    time_solved_in_contest = models.IntegerField(default=0)
    wrong_submissions_in_contest = models.IntegerField(default=0)

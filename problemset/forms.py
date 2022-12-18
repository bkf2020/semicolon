from django import forms

class ProblemForm(forms.Form):
    answer = forms.IntegerField(label='Your answer (should be an integer)')
    # id of the form above should be 'your_answer'

class MultipleChoiceForm(forms.Form):
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
    answer = forms.ChoiceField(widget=forms.RadioSelect, choices=ANSWER_CHOICES)
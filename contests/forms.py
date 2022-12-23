from django import forms

class RegisterForm(forms.Form):
    agree = forms.BooleanField(label="I agree to follow the rules")

class ProblemForm(forms.Form):
    answer = forms.IntegerField(label='Your answer (should be an integer)')
    problem_id = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'problemId'}))

class AIMEProblemForm(forms.Form):
    answer = forms.IntegerField(label='Your answer (should be an integer)', widget=forms.NumberInput(attrs={'autocomplete': 'off'}))
    problem_id = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'problemId'}))

class MultipleChoiceForm(forms.Form):
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('Blank', 'Blank')
    ]
    answer = forms.ChoiceField(label='Answer', widget=forms.RadioSelect(attrs={'class': 'answerForm'}), choices=ANSWER_CHOICES)
    problem_id = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class': 'problemId'}))
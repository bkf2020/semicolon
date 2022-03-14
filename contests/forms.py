from django import forms

class RegisterForm(forms.Form):
    agree = forms.BooleanField(label="I agree to follow the rules")

class ProblemForm(forms.Form):
    answer = forms.IntegerField(label='Your answer (should be an integer)')
    problem_id = forms.IntegerField(label='')

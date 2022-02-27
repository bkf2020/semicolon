from django import forms

class ProblemForm(forms.Form):
    answer = forms.IntegerField(label='Your answer (should be an integer)')
    # id of the form above should be 'your_answer'

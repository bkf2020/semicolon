from django import forms

class ProblemForm(forms.Form):
    answer = forms.IntegerField(label='Your answer (integer between 0 and 999 inclusive)', min_value=0, max_value=999)
    # id of the form above should be 'your_answer'

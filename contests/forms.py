from django import forms

class RegisterForm(forms.Form):
    agree = forms.BooleanField(label="I agree to follow the rules")

from django import forms
from django.contrib.auth.models import User

from .models import Employee


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control form-control-sm',}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control form-control-sm',}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control form-control-sm',}),
            'email' : forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'aria-describedby' : "emailHelp"}),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control form-control-sm', 'id' : 'exampleInputPassword1'}),

        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["designation"]
        widgets = {
            'designation' : forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }


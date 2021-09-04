from django import forms
from profile_app.forms import EmployeeForm, UserForm


class LoginForm(forms.Form):
    email = forms.EmailField(
        label = "Email Address", 
        widget = forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'id' : 'exampleInputEmail1', 'aria-describedby' : "emailHelp"})
    )
    login_password = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput(attrs={'class' : 'form-control form-control-sm', 'id' : 'exampleInputPassword1'})
    )

class EmployeePrileAppForm(EmployeeForm):
    pass

class UserProfileAppForm(UserForm):
    pass


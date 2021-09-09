from django import forms
from profile_app.forms import EmployeeForm, UserForm


class LoginForm(forms.Form):
    username = forms.CharField(
        label = "UserName",
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm',})
    )
    login_password = forms.CharField(
        label = "Password",
        widget = forms.PasswordInput(attrs={'class' : 'form-control form-control-sm', 'id' : 'exampleInputPassword1'})
    )

class EmployeePrileAppForm(EmployeeForm):
    pass

class UserProfileAppForm(UserForm):
    pass


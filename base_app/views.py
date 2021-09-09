from django.contrib.auth.models import User, auth
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView
from profile_app.models import Employee

from .forms import LoginForm
from .helper_function_modules.register_helper import *


class HomeTemplateView(TemplateView):
    template_name = "base_app/home.html"

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = "base_app/login.html"

class LoginCheckRedirectView(RedirectView):
        
    def get_redirect_url(self):
        try:
            username = LoginForm(self.request.POST).data.get('username')
            password = LoginForm(self.request.POST).data.get('login_password')

            user_verfied_obj = auth.authenticate(username=username, password=password)

            if user_verfied_obj and Employee.objects.get(user=user_verfied_obj).is_verified:
                auth.login(self.request, user_verfied_obj)
                return reverse("profile-detail", kwargs={'slug' : Employee.objects.get(user=user_verfied_obj).get_absolute_url()})
            elif not Employee.objects.get(user=user_verfied_obj).is_verified:
                messages.warning(self.request, "Account is not verified yet")
                return reverse("log-in")
            else:
                messages.warning(self.request, "Invalid Credentials")
                return reverse("log-in")

        except Exception:
            messages.warning(self.request, "Username is not registered! Register here")
            return reverse("register")

class LogoutRedirectView(RedirectView):
    url = "/"

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class TokenView(TemplateView):
    template_name = "base_app/token_send.html"

class SuccessView(TemplateView):
    template_name = "base_app/success.html"

class RegisterFormView(View):
    def get(self, request):
        return getFunction(request)

    def post(self, request):
        return postFunction(request)

class VerfifyRedirectView(RedirectView):
    url = "/login" # You add a slash in front of the url you want to redirect to like this + app/ in urlpattern

    def get_redirect_url(self, **kwargs):
        auth_token = kwargs['auth_token']
        employee_obj = get_object_or_404(Employee, auth_token=auth_token)

        if employee_obj:
            employee_obj.is_verified = True
            employee_obj.save()

        messages.info(self.request, "Account is now verified!")

        return super().get_redirect_url(**kwargs)

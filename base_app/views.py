from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import FormView
from profile_app.models import Employee

from .forms import LoginForm
from .helper_modules.helper_function_views import *

is_login = False
# Create your views here.
class HomeTemplateView(TemplateView):
    template_name = "base_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global is_login
        context['is_login'] = is_login
        return context

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = "base_app/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global is_login
        context['is_login'] = is_login
        return context


class LoginCheckRedirectView(RedirectView):
    form_class = LoginForm

    def get_redirect_url(self, *args, **kwargs):
        try:
            global is_login
            email = self.form_class(self.request.POST).data.get('email')
            password = self.form_class(self.request.POST).data.get('login_password')

            user_obj = User.objects.filter(email=email).first()
            user_obj = user_obj if user_obj.check_password(password) else None
            if user_obj:
                employee_obj = Employee.objects.filter(user=user_obj, is_verified=True).first()
                if employee_obj:
                    is_login = True
                    return reverse("profile-detail", kwargs={'slug' : employee_obj.slug})
                else:
                    messages.warning(self.request, "Account is not verfied yet!")
                    return reverse("log-in")
            else:
                messages.warning(self.request, "Invalid Email or Password!")
                return reverse("log-in")

        except Exception:
            messages.warning(self.request, "Username is not registered!")
            return reverse("log-in")

class LogoutRedirectView(RedirectView):
    url = "/"

    def get_redirect_url(self, *args, **kwargs):
        global is_login
        logout(self.request)
        is_login = False
        return super().get_redirect_url(*args, **kwargs)

class TokenView(TemplateView):
    template_name = "base_app/token_send.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global is_login
        context['is_login'] = is_login
        return context


class SuccessView(TemplateView):
    template_name = "base_app/success.html"

class RegisterFormView(View):
    global is_login
    def get(self, request):
        return getFunction(request, is_login)

    def post(self, request):
        return postFunction(request)

class VerfifyRedirectView(RedirectView):
    url = "/login" # You add a slash in front of the url you want to redirect to like this + app/ in urlpattern

    def get_redirect_url(self, **kwargs):
        user_obj = get_object_or_404(Employee, auth_token=kwargs['auth_token'])
        user_obj.is_verified = True
        user_obj.save()

        messages.info(self.request, "Account is now verified!")

        return super().get_redirect_url(**kwargs)

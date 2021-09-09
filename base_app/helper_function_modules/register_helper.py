import uuid

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from profile_app.models import Designation, Employee

from ..forms import EmployeePrileAppForm, UserProfileAppForm


def getFunction(request):
    form_list = [UserProfileAppForm, EmployeePrileAppForm]
    return render(request, "base_app/register.html", {
        "forms" : form_list,
    })

def postFunction(request):
    user_form = UserProfileAppForm(request.POST)
    emp_form = EmployeePrileAppForm(request.POST, request.FILES)

    if user_form.is_valid() and emp_form.is_valid():
        username = user_form.cleaned_data['username']
        first_name = user_form.cleaned_data['first_name']
        last_name = user_form.cleaned_data['last_name']
        email = user_form.cleaned_data['email']
        password = user_form.cleaned_data['password']
        designation = emp_form.cleaned_data['designation']
        image = emp_form.cleaned_data['image']

        if User.objects.filter(email=email).first():
            messages.warning(request, "Email is already taken!")
            return HttpResponseRedirect(reverse("register"))

        auth_token = str(uuid.uuid4())[:4]
        user_obj = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)

        designation_obj = Designation.objects.get(position=designation)

        employee_obj = Employee(user=user_obj, auth_token=auth_token, designation=designation_obj, image=image)
        employee_obj.save()

        send_verification_mail(request, username, email, auth_token)

        return HttpResponseRedirect(reverse("token"))
    else:
        messages.warning(request, "Username is already taken!")
        return HttpResponseRedirect(reverse("register"))

def send_verification_mail(request, username, email, token):
    subject = "Welcome to Software Giant"
    current_domain = get_current_site(request)
    message = f"Hi {username}, thank you for registering in Software Giant and click the link to verfiy your email {current_domain}/verfiy/{token}"
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_form, recipient_list)


def logout(request):
    auth.logout(request)


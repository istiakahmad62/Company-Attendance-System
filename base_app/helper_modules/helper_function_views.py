import uuid

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.models import User  # ----------
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from profile_app.models import Designation, Employee

from ..forms import EmployeePrileAppForm, UserProfileAppForm


def getFunction(request, is_login):
    form_list = [UserProfileAppForm, EmployeePrileAppForm]
    return render(request, "base_app/register.html", {
        "forms" : form_list,
        "is_login" : is_login,
    })

def postFunction(request):
    username = request.POST['username']
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password = request.POST['password']
    designation_id = request.POST['designation']

    # print(f"{username} designation {designation_id}")
    
    if User.objects.filter(Q(username=username) | Q(email=email)).first():
        messages.warning(request, "Username or Email is already taken!")
        return HttpResponseRedirect(reverse("register"))
    
    user_obj = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
    user_obj.set_password(password)
    user_obj.save()

    designation_obj = Designation.objects.get(id=int(designation_id))

    # print(designation_obj)
    
    auth_token = str(uuid.uuid4())[:5]
    employee_obj = Employee(user=user_obj, auth_token=auth_token, designation=designation_obj)
    employee_obj.save()

    send_verification_mail(request, username, email, auth_token)
    
    return HttpResponseRedirect(reverse("token"))

def send_verification_mail(request, username, email, token):
    subject = "Welcome to Software Giant"
    current_domain = get_current_site(request)
    message = f"Hi {username}, thank you for registering in Software Giant and click the link to verfiy your email {current_domain}/verfiy/{token}"
    # print(message)
    email_form = settings.EMAIL_HOST_USER
    # print(email_form)
    recipient_list = [email,]
    send_mail(subject, message, email_form, recipient_list)

def logout(request):
    auth.logout(request)


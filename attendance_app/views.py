import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from profile_app.models import Employee
from profile_app.views import is_linkActive

from .forms import AttendanceForm
from .models import Attendance


# Create your views here.
class AttendanceFormCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = "attendance_app/attendance-form.html"

    def form_valid(self, form):
        form.save(commit=False)
        global is_linkActive
        emp_obj = Employee.objects.filter(slug=self.kwargs.get('slug')).first()
        form.instance.emp_id = emp_obj
        form.instance.date = datetime.date.today()
        is_linkActive = False
        form.save()

        return HttpResponseRedirect(reverse("profile-detail", kwargs={'slug' : emp_obj.slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = datetime.date.today()
        context['emp'] = Employee.objects.filter(slug=self.kwargs.get('slug')).first()
        context['is_login'] = True
        return context


import datetime
import time
from calendar import monthrange

from attendance_app.forms import AttendanceForm
from django.shortcuts import render
from django.views.generic import DetailView

from .models import Employee

is_linkActive = False

# Create your views here.
class ProfileDetailView(DetailView):
    model = Employee
    template_name = "profile_app/profile-detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        emp_obj = Employee.objects.filter(slug=self.kwargs.get('slug')).first()
        qs = emp_obj.attendances.all()
        attendance_count = 0
        for q in qs:
            if q.isPresent:
                attendance_count += 1

        dt = datetime.datetime.today()
        year, month = dt.year, dt.month
        days = monthrange(year, month)

        salary = emp_obj.designation.salary
        curr_salary = ((salary*attendance_count)/(days[1]-8))
        attendance_percentange = (attendance_count/(days[1]-8)) * 100

        curr_time = time.localtime()
        hour = time.strftime("%H", curr_time)
        minute = time.strftime("%M", curr_time)

        global is_linkActive
        if is_linkActive == True or emp_obj.attendances.filter(date=datetime.date.today(), isPresent=True).first():
            is_linkActive = False
        elif is_linkActive == False and (int(hour) == 10 and 0 <= int(minute) <= 30 and (not emp_obj.attendances.filter(date=datetime.date.today(), isPresent=True).first())):
            is_linkActive = True

        context['form'] = AttendanceForm
        context['is_login'] = True
        context['emp'] = emp_obj
        context['curr_salary'] = round(curr_salary, 2)
        context['attendace_percent'] = round(attendance_percentange, 2)
        context['is_linkActive'] = is_linkActive
        return context
 
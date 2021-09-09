import datetime
import time
from calendar import monthrange

from attendance_app.forms import AttendanceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from .models import Employee

is_linkActive = False

class ProfileDetailView(LoginRequiredMixin, DetailView):
    login_url = "log-in"
    model = Employee
    template_name = "profile_app/profile-detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        global is_linkActive
        # from database
        emp_obj = Employee.objects.filter(slug=self.kwargs.get('slug')).first()
        salary = emp_obj.designation.salary
        qs = emp_obj.attendances.all()
        attendance_count = 0
        for q in qs:
            if q.isPresent:
                attendance_count += 1

        # date-time
        dt = datetime.datetime.today()
        year, month = dt.year, dt.month
        days = monthrange(year, month)

        curr_day = datetime.date.today().strftime("%A").lower()

        curr_time = time.localtime()
        hour = time.strftime("%H", curr_time)
        minute = time.strftime("%M", curr_time)

        # salary calculation
        curr_salary = ((salary*attendance_count)/(days[1]-8))
        attendance_percentange = (attendance_count/(days[1]-8)) * 100

        if is_linkActive == True or emp_obj.attendances.filter(date=datetime.date.today(), isPresent=True).first() or (curr_day == "friday" or curr_day == "saturday"):
            is_linkActive = False
        elif is_linkActive == False and (int(hour) == 10 and 0 <= int(minute) <= 30 and (not emp_obj.attendances.filter(date=datetime.date.today(), isPresent=True).first())):
            is_linkActive = True

        context['form'] = AttendanceForm
        context['curr_salary'] = round(curr_salary, 2)
        context['attendace_percent'] = round(attendance_percentange, 2)
        context['is_linkActive'] = is_linkActive
        return context
 
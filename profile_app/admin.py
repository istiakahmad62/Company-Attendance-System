from django.contrib import admin

from .models import Designation, Employee

# Register your models here.
admin.site.register(Employee)
admin.site.register(Designation)

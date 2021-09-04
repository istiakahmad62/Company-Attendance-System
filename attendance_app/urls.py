from django.urls import path

from . import views

urlpatterns = [
    path('<slug:slug>', views.AttendanceFormCreateView.as_view(), name='attendance-form'),
]

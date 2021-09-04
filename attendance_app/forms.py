from django import forms

from .models import Attendance


class PresentSelectInput(forms.CheckboxInput):
    input_type = "checkbox"

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["isPresent",]
        labels = {
            'isPresent' : 'Present(select checkbox)'
        }
        widgets = {
            'isPresent' : PresentSelectInput
        }

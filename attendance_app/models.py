from django.db import models
from profile_app.models import Employee

# Create your models here.

class Attendance(models.Model):
    date = models.DateField()
    isPresent = models.BooleanField(default=False)
    emp_id = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE, related_name="attendances")

    def __str__(self):
        return f"{self.date} {self.isPresent}"

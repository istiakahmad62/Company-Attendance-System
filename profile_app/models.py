from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Designation(models.Model):
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.position

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users")
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    designation = models.OneToOneField(Designation, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="images", null=True)
    slug = models.SlugField(default="", unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify((self.user.first_name + self.user.last_name))
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return self.slug #reverse("profile-detail", kwargs={'slug':self.slug})

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

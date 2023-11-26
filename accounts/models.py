from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, 
                              on_delete=models.CASCADE)
    image=models.ImageField(upload_to="users/", null=True, blank=True)
    date_of_birth=models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} profili"
    

    
    
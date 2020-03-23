from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Todo(models.Model):
    todotitle=models.CharField(max_length=300)
    category=models.CharField(max_length=100)
    notes=models.CharField(max_length=1024)
    # event=models.CharField(max_length=100, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    completed=models.DateTimeField(null=True, blank=True)
    important=models.BooleanField(default=False)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.todotitle

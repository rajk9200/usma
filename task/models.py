from django.db import models

# Create your models here.

import uuid
class Task(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now=True)
    status =models.BooleanField(default=True)



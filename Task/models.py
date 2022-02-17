
from django.db import models
from django.core.validators import MinLengthValidator,MinValueValidator,MaxLengthValidator


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name =models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.IntegerField()
    email = models.EmailField()
    web = models.URLField()
    age = models.IntegerField()

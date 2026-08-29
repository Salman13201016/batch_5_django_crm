from django.db import models

# Create your models here.
#oop = design pattern of coding

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    sort_order = models.CharField(unique=True)
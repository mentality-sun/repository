from django.db import models
class Regists(models.Model):
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    repassword = models.CharField(max_length=64)

# Create your models here.
class menu (models.Model):
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=64)
    number = models.CharField(max_length=64)
    path = models.CharField(max_length=128)
class house(models.Model):
    cname=models.CharField(max_length=64)
    price=models.CharField(max_length=64)
    hnumber=models.CharField(max_length=64)
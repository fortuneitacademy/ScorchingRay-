from dataclasses import fields
from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.
class Student(models.Model):
    url_img = models.URLField()
    img_name = models.CharField(max_length=500) 
    url_stl = models.URLField()
    
class UploadModel(models.Model):
    file = models.FileField()



from django.db import models

# Create your models here.

class New(models.Model):
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=5)
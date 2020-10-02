from django.db import models

# Create your models here.

class New(models.Model):
    """
    Model class for New
    """
    title = models.CharField(max_length=255)
    tag = models.CharField(max_length=5)


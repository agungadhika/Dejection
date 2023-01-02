from django.db import models

# Create your models here.
class xss(models.Model):
    payload = models.CharField(max_length=255)

class commandinjection(models.Model):
    payload = models.CharField(max_length=255)

class sqlinjection(models.Model):
    payload = models.CharField(max_length=255)

class nosqlinjection(models.Model):
    payload = models.CharField(max_length=255)

class xxeinjection(models.Model):
    payload = models.CharField(max_length=255)

from django.db import models


class Rental(models.Model):
    title = models.CharField(max_length=1024)
    owner = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024)
    image = models.CharField(max_length=1024)
    bedrooms = models.CharField(max_length=1024)

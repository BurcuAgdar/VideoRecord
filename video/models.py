from django.db import models

class CountModel(models.Model):
    count=models.IntegerField(default=0)

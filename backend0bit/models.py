from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    contents = models.TextField()
    date = models.DateField()

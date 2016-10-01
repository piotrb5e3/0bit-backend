from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    contents = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class StaticPage(models.Model):
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=64, unique=True)
    contents = models.TextField()

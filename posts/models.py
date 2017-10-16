from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    contents = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    last_edited_date = models.DateTimeField(null=True, blank=True,
                                            default=None)

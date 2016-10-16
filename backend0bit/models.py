from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=256)
    contents = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


class StaticPage(models.Model):
    title = models.CharField(max_length=256)
    url = models.CharField(max_length=64, unique=True)
    contents = models.TextField()
    order = models.IntegerField(unique=True, default=lambda: StaticPage.get_max_order_or_zero() + 1)

    @classmethod
    def get_max_order_or_zero(cls):
        x = cls.objects.all().aggregate(models.Max('order'))["order__max"]
        if x is None:
            return 0
        else:
            return x

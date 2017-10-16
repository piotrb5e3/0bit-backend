from django.db import models


def get_next_order():
    return StaticPage.get_max_order_or_zero() + 1


class StaticPage(models.Model):
    @classmethod
    def get_max_order_or_zero(cls):
        x = cls.objects.all().aggregate(models.Max('order'))["order__max"]
        if x is None:
            return 0
        else:
            return x

    title = models.CharField(max_length=256)
    url = models.CharField(max_length=64, unique=True)
    contents = models.TextField()
    order = models.IntegerField(
        unique=True,
        default=get_next_order
    )

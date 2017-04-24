from django.db import transaction
from backend0bit.models import StaticPage


@transaction.atomic
def set_staticpage_order(order):
    _sanitize_order_list(order)
    _set_safe_order_values()

    counter = 0

    for sp_id in order:
        sp = StaticPage.objects.get(id=sp_id)
        sp.order = counter
        sp.save()
        counter += 1


def _sanitize_order_list(order):
    if len(order) != StaticPage.objects.count():
        raise ReorderException("Incorrect number of orders")
    sp_ids = [x["id"] for x in StaticPage.objects.all().values("id")]
    for sp_id in sp_ids:
        if sp_id not in order:
            raise ReorderException('Id ' + str(sp_id) + ' not in passed order')


def _set_safe_order_values():
    max_order = StaticPage.get_max_order_or_zero()
    for sp in StaticPage.objects.all():
        sp.order += max_order + 1
        sp.save()


class ReorderException(BaseException):
    cause = None

    def __init__(self, cause):
        self.cause = cause

    def get_cause(self):
        return self.cause

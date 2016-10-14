import json
import sys
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend0bit.models import Post, StaticPage
from backend0bit.serializers import PostSerializer, StaticPageSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StaticPageViewSet(viewsets.ModelViewSet):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('url',)


@api_view(['POST'])
def reorder_staticpages(request):
    try:
        order = _get_order_from_request(request)
        _set_staticpage_order(order)
        return Response("Successful" , status=status.HTTP_200_OK)
    except ReorderException:
        return Response(sys.exc_info()[1].get_cause(), status=status.HTTP_400_BAD_REQUEST)


class ReorderException(BaseException):
    cause = None

    def __init__(self, cause):
        self.cause = cause

    def get_cause(self):
        return self.cause


def _get_order_from_request(request):
    try:
        order = json.loads(request.body.decode()).get('order')
    except json.decoder.JSONDecodeError:
        raise ReorderException("Passed data structure incorrect")

    try:
        return [int(x) for x in order]
    except ValueError:
        raise ReorderException("Passed data structure incorrect")


def _set_staticpage_order(order):
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
    max_order = StaticPage.get_max_order()
    for sp in StaticPage.objects.all():
        sp.order += max_order + 1
        sp.save()

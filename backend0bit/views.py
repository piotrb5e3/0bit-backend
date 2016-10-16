import json
import sys
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend0bit.models import Post, StaticPage
from backend0bit.serializers import PostSerializer, StaticPageSerializer
from backend0bit import reorder


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
        reorder.set_staticpage_order(order)
        return Response("Successful", status=status.HTTP_200_OK)
    except reorder.ReorderException:
        return Response(sys.exc_info()[1].get_cause(), status=status.HTTP_400_BAD_REQUEST)


def _get_order_from_request(request):
    try:
        order = json.loads(request.body.decode()).get('order')
    except json.decoder.JSONDecodeError:
        raise reorder.ReorderException("Passed data structure not in JSON form")

    try:
        return [int(x) for x in order]
    except ValueError:
        raise reorder.ReorderException("Passed data structure incorrect")

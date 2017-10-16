import json
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from backend0bit.models import StaticPage
from backend0bit.serializers import StaticPageSerializer
from backend0bit import reorder


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
    except reorder.ReorderException as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


def _get_order_from_request(request):
    try:
        order = json.loads(request.body.decode()).get('order')
    except json.decoder.JSONDecodeError:
        raise reorder.ReorderException(
            "Passed data structure not in JSON format"
        )

    try:
        return [int(x) for x in order]
    except ValueError:
        raise reorder.ReorderException("Passed data structure incorrect")


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_status(request):
    return Response("OK")

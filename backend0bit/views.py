from backend0bit.models import Post, StaticPage
from backend0bit.serializers import PostSerializer, StaticPageSerializer
from rest_framework import viewsets, permissions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StaticPageViewSet(viewsets.ModelViewSet):
    queryset = StaticPage.objects.all()
    serializer_class = StaticPageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('url',)

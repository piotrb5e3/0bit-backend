from rest_framework import viewsets, permissions

from .serializers import PostSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

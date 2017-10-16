from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from .serializers import PostSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(methods=['post'],
                  permission_classes=(permissions.IsAuthenticated, ))
    def publish(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if post.published:
            return Response("Post already published",
                            status=status.HTTP_400_BAD_REQUEST)

        post.published = True
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'],
                  permission_classes=(permissions.IsAuthenticated, ))
    def unpublish(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if not post.published:
            return Response("Post already unpublished",
                            status=status.HTTP_400_BAD_REQUEST)

        post.published = False
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

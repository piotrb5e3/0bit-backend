from rest_framework import serializers
from backend0bit.models import Post, StaticPage


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'contents', 'date')
        read_only_fields = ('date',)


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ('id', 'title', 'url', 'contents')

from rest_framework import serializers
from backend0bit.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'contents', 'date')
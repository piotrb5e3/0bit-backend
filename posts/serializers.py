import pytz

from datetime import datetime
from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'contents', 'date', 'last_edited_date')
        read_only_fields = ('date', 'last_edited_date')

    def update(self, instance, validated_data):
        instance.last_edited_date = datetime.utcnow().replace(tzinfo=pytz.UTC)
        instance = super().update(instance, validated_data)
        return instance

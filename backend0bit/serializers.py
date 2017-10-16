from rest_framework import serializers

from backend0bit.models import StaticPage


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ('id', 'title', 'url', 'contents', 'order')
        read_only_fields = ('order',)

from rest_framework import serializers

from scidash.general.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )

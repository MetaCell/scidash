from rest_framework import serializers

from general.models import ScidashUser


class ScidashUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScidashUser
        fields = '__all__'

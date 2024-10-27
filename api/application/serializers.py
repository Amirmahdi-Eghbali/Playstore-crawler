from rest_framework import serializers
from .models import AppId


class AppIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppId
        field = '__all__'

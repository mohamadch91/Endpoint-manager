
from rest_framework import serializers

from .models import Warning

class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warning
        fields = ['pk','url','created_at','updated_at']
        extra_kwargs = {
            'url': {'required': True},
        }
        read_only_fields = ['created_at','updated_at']

class GetWarningSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200,required=True)
    
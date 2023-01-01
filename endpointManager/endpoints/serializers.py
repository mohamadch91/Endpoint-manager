
from rest_framework import serializers

from .models import Url

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['pk','url','user','fail_limit','success_count','fail_count','created_at','updated_at']
        extra_kwargs = {
            'url': {'required': True},
            'user': {'required': True},
            'fail_limit': {'required': True},
        }
        read_only_fields = ['created_at','updated_at']
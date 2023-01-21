
from rest_framework import serializers

from .models import Endpoint,Request

class EndpointRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['id','address','user','fail_limit','created_at','updated_at']
        extra_kwargs = {
            'address': {'required': True},
            'user': {'required': True},
            'fail_limit': {'required': True},
        }
        read_only_fields = ['created_at','updated_at']
class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['id','address','fail_limit','created_at','updated_at']
        extra_kwargs = {
            'address': {'required': True},
            'fail_limit': {'required': True},
        }
        read_only_fields = ['created_at','updated_at']

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id','endpoint','status_code','created_at','updated_at']
        extra_kwargs = {
            'enpoint': {'required': True},
            'status_code': {'required': True},
        }
        read_only_fields = ['created_at','updated_at']

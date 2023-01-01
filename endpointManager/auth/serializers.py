
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from authen.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

import json



 ## define the serializer class for Ueser model    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','password','owner','is_active','is_superuser','name','facilityid','username','idnumber','position','phone','facadmin','itemadmin','reportadmin','useradmin','created_at','updated_at']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['created_at','updated_at']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['pk','password','owner','is_active','name','facilityid','username','idnumber','position','phone','facadmin','itemadmin','reportadmin','useradmin','created_at','updated_at']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# user update serilizer         
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','password','is_active','name','facilityid','username','idnumber','position','phone','facadmin','itemadmin','reportadmin','useradmin','created_at','updated_at']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': False},
        }

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)    
                
        
    
    def update(self, instance, validated_data):
        new_data={}
        for key in validated_data.keys():
            if validated_data[key] != None and validated_data[key] != "":
                new_data[key]=validated_data[key]      
        instance=super().update(instance, new_data)
        instance.save()
        return instance    
# user change password serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password')

    def validate(self, attrs):
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()
        return instance      

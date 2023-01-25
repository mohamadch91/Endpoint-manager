
from rest_framework import serializers
from .models import User



 ## define the serializer class for Ueser model    
class UserSerializer(serializers.ModelSerializer):
    """User serializer class

    Args:
        serializers (Django serializers): serilize the model
    """
    class Meta:
        """Meta class for UserSerializer
        """
        model = User
        fields = ['pk','name','username','password','created_at','updated_at']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['created_at','updated_at']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    """Register serializer class for User registration

    Args:
        serializers (Django serializer): serialize the model

    Returns:
        _type_: User model
    """
    
    class Meta:
        model = User
        fields = ['pk','name','username','password','created_at','updated_at']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data: dict) -> User:
        """
        Create and return a new `User` instance, given the validated data.
        """
        user = User.objects.create_user(**validated_data)
        return user


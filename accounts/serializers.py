from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
    
class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    profile_image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'profile_image')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])

        user.save()
        return user
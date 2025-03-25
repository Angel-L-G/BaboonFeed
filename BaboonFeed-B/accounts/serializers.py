from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'confirmPassword']

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise ValidationError
        return data

    def create(self, validated_data):
        validated_data.pop('confirmPassword')
        user = get_user_model().objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user

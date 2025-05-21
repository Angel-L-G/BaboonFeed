from rest_framework import serializers
from .models import User

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar']

class UserDetailSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'bio', 'followers', 'following']

    def get_followers(self, obj):
        return [f.followed_by.username for f in obj.followed_by.all()]

    def get_following(self, obj):
        return [f.following.username for f in obj.following.all()]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['bio', 'avatar']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'avatar']
from rest_framework import serializers
from users.models import User

from .models import GroupChat


class GroupUserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'avatar']

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class GroupChatSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    leader = GroupUserSerializer(read_only=True)
    members = GroupUserSerializer(many=True, read_only=True)

    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'avatar_url', 'last_message', 'last_modified', 'leader', 'members']

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_last_message(self, obj):
        return obj.last_message.content if obj.last_message else None


class GroupChatCreateUpdateSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True, slug_field='username', queryset=User.objects.all(), required=False
    )

    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'avatar', 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        user = self.context['request'].user
        group = GroupChat.objects.create(leader=user, **validated_data)
        for username in members_data:
            member = User.objects.filter(username=username).first()
            if member:
                group.members.add(member)

        return group

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members', None)
        instance.name = validated_data.get('name', instance.name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        if members_data:
            instance.members.clear()
            for member in members_data:
                instance.members.add(member)
        return instance

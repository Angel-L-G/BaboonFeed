from chats.serializers import MessageSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shared.views import CustomLimitOffsetPagination

from .models import GroupChat
from .permissions import IsGroupLeader
from .serializers import GroupChatCreateUpdateSerializer, GroupChatSerializer, GroupUserSerializer


class GroupChatViewSet(viewsets.ViewSet):
    permission_classes = [
        IsAuthenticated,
        IsGroupLeader,
    ]  # Se requiere estar autenticado y ser líder para hacer modificaciones

    # GET /groups/
    def list(self, request):
        groups = GroupChat.objects.filter(members=request.user).union(
            GroupChat.objects.filter(leader=request.user).order_by('-last_modified')
        )
        serializer = GroupChatSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)

    # GET /groups/<pk>/
    def retrieve(self, request, pk=None):
        group = get_object_or_404(GroupChat, pk=pk)
        self.check_object_permissions(request, group)
        serializer = GroupChatSerializer(group, context={'request': request})
        return Response(serializer.data)

    # POST /groups/
    def create(self, request):
        serializer = GroupChatCreateUpdateSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            group = serializer.save()
            output_serializer = GroupChatSerializer(group, context={'request': request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT /groups/<pk>/
    def update(self, request, pk=None):
        group = get_object_or_404(GroupChat, pk=pk)
        serializer = GroupChatCreateUpdateSerializer(
            group, data=request.data, context={'request': request}
        )
        self.check_object_permissions(request, group)
        if serializer.is_valid():
            group = serializer.save()
            output_serializer = GroupChatSerializer(group, context={'request': request})
            return Response(output_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET /groups/<pk>/members
    @action(detail=True, methods=['get'], url_path='members')
    def members(self, request, pk=None):
        group = get_object_or_404(GroupChat, pk=pk)
        self.check_object_permissions(request, group)
        group_members = group.members.all()
        data = {}
        members = []
        for member in group_members:
            members.append(GroupUserSerializer(member, context={'request': request}).data)
        data['members'] = members
        data['leader'] = GroupUserSerializer(group.leader, context={'request': request}).data
        return Response(data)

    # DELETE /groups/<pk>/leave/ - permite abandonar el grupo
    @action(detail=True, methods=['delete'], url_path='leave')
    def leave(self, request, pk=None):
        group = get_object_or_404(GroupChat, pk=pk)
        self.check_object_permissions(request, group)
        user = request.user
        if not group.leader == user:
            group.members.remove(user)
            return Response(
                {'detail': f'Member {user.username} has left the group.'}, status=status.HTTP_200_OK
            )

        remaining_members = group.members.all()
        if remaining_members.exists():
            import random

            new_leader = random.choice(remaining_members)
            group.leader = new_leader
            group.save()
            return Response(
                {
                    'detail': f'Leader {user.username} has left the group. Assigned {new_leader.username} as Leader'
                },
                status=status.HTTP_200_OK,
            )

        group.delete()
        return Response(
            {
                'detail': f'Group {group.name} has been deleted because the leader left and there are no remaining members.'
            },
            status=status.HTTP_200_OK,
        )

    # GET /api/chats/<id>/messages/?limit=20&offset=0/
    @action(detail=True, methods=['get'], url_path='messages')
    def messages(self, request, pk=None):
        group = get_object_or_404(GroupChat, pk=pk)
        self.check_object_permissions(request, group)
        messages = group.messages.all().order_by('-created_at')

        paginator = CustomLimitOffsetPagination()
        paginated_qs = paginator.paginate_queryset(messages, request)

        serializer = MessageSerializer(paginated_qs, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

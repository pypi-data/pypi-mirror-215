from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.mixins import (
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from permissions_management.api.permissions import InstancePermission, IsMember
from permissions_management.api.serializers import (
    GroupGetSerializer,
    GroupSerializer,
    ContentTypeSerializer,
    PermissionPostSerializer,
    PermissionSerializer,
)
from permissions_management.utils import (
    GroupViewSetConstants,
    ContentTypeListViewConstants,
    PermissionViewSetConstants,
    UserPermissionListViewConstants,
)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_required = GroupViewSetConstants.permission_required
    permission_classes = [InstancePermission, IsMember]

    def get_serializer_class(self):
        """dynamic serializer to return serializer based on the action requested"""
        if self.request.method in SAFE_METHODS:
            return GroupGetSerializer
        return GroupSerializer


class ContentTypeViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ContentType.objects.all()
    permission_required = ContentTypeListViewConstants.permission_required
    serializer_class = ContentTypeSerializer


class PermissionViewSet(
    GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
):
    queryset = Permission.objects.all()
    permission_required = PermissionViewSetConstants.permission_required

    def get_serializer_class(self):
        if self.action == "create":
            return PermissionPostSerializer
        return PermissionSerializer

    def perform_create(self, serializer):
        try:
            content_type = ContentType.objects.get(
                id=serializer.validated_data.get("content_type_id")
            )
            serializer.save(content_type=content_type)
        except ContentType.DoesNotExist as e:
            raise serializers.ValidationError(e)


class UserPermissionListView(ListAPIView):
    serializer_class = PermissionSerializer
    permission_required = UserPermissionListViewConstants.permission_required

    def get_queryset(self):
        user = self.request.user
        permissions = user.user_permissions.all()
        return permissions

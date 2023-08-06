from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    """Serializer for permission response"""

    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]

    def validate_codename(self, value):
        """method to check if the posted codename exist within the same content type or not"""
        content_type_id = self.initial_data.get("content_type_id")
        if Permission.objects.filter(codename=value, content_type__id=content_type_id):
            raise serializers.ValidationError(
                "Duplicate codename. Please try different codename"
            )
        return value


class PermissionPostSerializer(PermissionSerializer):
    """Serializer for permission creation"""

    content_type_id = serializers.IntegerField(required=True, write_only=True)

    class Meta(PermissionSerializer.Meta):
        fields = PermissionSerializer.Meta.fields + ["content_type_id"]


class ContentTypeSerializer(serializers.ModelSerializer):
    """Serializer for contenttype with permissions response"""

    permission_set = PermissionSerializer(many=True)

    class Meta:
        model = ContentType
        fields = ("id", "name", "app_label", "permission_set")


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for group response"""

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class GroupGetSerializer(serializers.ModelSerializer):
    """Serializer for group creation"""

    permissions = PermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

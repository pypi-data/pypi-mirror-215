from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import BasePermission

from permissions_management.utils import get_instance_permission, check_user_permissions


class CustomRolesPermissions(BasePermission):
    """
    Custom permission class to check if user has the required permission to proceed.
    """

    def __verify_permission_required_property(self, view):
        """
        verifies presence of required permissions attribute in view if not then throw error.
        :param view:
        :return iterable:
        """
        if not hasattr(view, "permission_required"):
            raise ImproperlyConfigured(
                "{0} is missing the permission_required attribute."
                " Define {0}.permission_required, or override "
                "{0}.get_permission_required().".format(self.__class__.__name__)
            )

    def get_permissions_required(self, method, view):
        """
        returns the required permissions written in permission required attribute
        :param method:
        :param view:
        :return iterable:
        """
        self.__verify_permission_required_property(view)
        permission_required = view.permission_required
        if isinstance(permission_required, str):
            perms = (permission_required,)
        elif isinstance(permission_required, dict):
            perms = permission_required.get(method, ())
            if not (isinstance(perms, tuple) or isinstance(perms, list)):
                raise ImproperlyConfigured(
                    "{} has Invalid Permissions defined in the permission_required. "
                    "Key must be a proper request method and value must be list or tuple"
                    "Request method {} and method permissions {}".format(
                        self.__class__.__name__,
                        self.request.method,
                        perms,
                    )
                )
        else:
            perms = permission_required
        return perms

    def has_permission(self, request, view):
        perms = self.get_permissions_required(request.method, view)
        return bool(
            request.user and request.user.is_authenticated
        ) and request.user.has_perms(perms)


class InstancePermission(BasePermission):
    """
    Custom permission class to check if user has the required permission to proceed.
    """

    def has_permission(self, request, view):
        """method to check if CustomRolesPermissions should be involved or not."""
        if view.action in ["list", "create"]:
            return CustomRolesPermissions().has_permission(request, view)
        return True

    def has_object_permission(self, request, view, obj):
        """
        returns the required permissions written in permission required attribute
        :param request:
        :param view:
        :param obj:
        :return bool:
        condition 1: has_group_permissions and has_instance_permission: Allow
        condition 2: not has_group_permissions and has_instance_permission: Allow
        condition 3: has_group_permissions and not has_instance_permission: Do Not Allow
        condition 4: has_group_permissions and not has_instance_permission: Do Not Allow
        """
        user = request.user
        instance_permission = Permission.objects.filter(
            codename=get_instance_permission(request.method, obj)
        )
        return (
            user.is_authenticated
            and check_user_permissions(user, instance_permission)
            and bool(
                CustomRolesPermissions().has_permission(request, view)
                or check_user_permissions(user, instance_permission)
            )
        )


class IsMember(BasePermission):
    """
    A permission class to check whether the user operating on a role or instance is a part of that instance or not
    """

    def has_object_permission(self, request, view, obj):
        """
        method to check whether the user operating on a role or instance is a part of that instance or not
        """
        return request.user in obj.user_set.all()

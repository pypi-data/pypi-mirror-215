class GroupViewSetConstants:
    """class for declaring required permissions for user to operate on groups"""

    permission_required = {
        "GET": (
            "auth.view_group",
            "auth.view_permission",
        ),
        "POST": (
            "auth.add_group",
            "auth.add_permission",
        ),
        "PUT": (
            "auth.change_group",
            "auth.add_permission",
            "auth.change_permission",
        ),
        "PATCH": (
            "auth.change_group",
            "auth.add_permission",
            "auth.change_permission",
        ),
        "DELETE": (
            "auth.delete_group",
            "auth.delete_permission",
        ),
    }


class ContentTypeListViewConstants:
    """class for declaring required permissions for user to operate on content types"""

    permission_required = {"GET": ("contenttypes.view_contenttype",)}


class PermissionViewSetConstants:
    """need permissions for a user to CRUD on permission instance/instances."""

    permission_required = {
        "GET": ("auth.view_permission",),
        "POST": ("auth.add_permission",),
        "PUT": ("auth.change_permission",),
        "PATCH": ("auth.change_permission",),
        "DELETE": ("auth.delete_permission",),
    }


class UserPermissionListViewConstants:
    """class for declaring required permissions for user to operate on permissions"""

    permission_required = {"GET": ("auth.view_permission",)}


PERMISSION_METHOD_MAPPER = {
    "GET": "view_{}",
    "POST": "add_{}",
    "PUT": "change_{}",
    "PATCH": "change_{}",
    "DELETE": "delete_{}",
}


def get_instance_permission(method, obj):
    """get the instance permissions based on the type of request method user asked for."""
    permission = PERMISSION_METHOD_MAPPER.get(method).format(
        obj.__class__.__name__.lower()
    )
    return permission


def check_user_permissions(user, required_permissions):
    """check whether the user possess required permissions or not."""
    user_permissions_count = user.user_permissions.filter(
        id__in=required_permissions
    ).count()
    return user_permissions_count == required_permissions.count()

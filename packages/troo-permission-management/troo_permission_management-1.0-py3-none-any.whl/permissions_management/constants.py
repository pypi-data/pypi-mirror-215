from enum import Enum

from django.shortcuts import reverse


class PermissionMessagesEnum(Enum):
    PERMISSION_DENIED_MESSAGE = "You do not have permission to perform this action."


class PermissionsEnum(Enum):
    VIEW_GROUP = "view_group"
    ADD_GROUP = "add_group"
    CHANGE_GROUP = "change_group"
    DELETE_GROUP = "delete_group"
    ADD_PERMISSION = "add_permission"
    VIEW_PERMISSION = "view_permission"
    CHANGE_PERMISSION = "change_permission"
    DELETE_PERMISSION = "delete_permission"
    VIEW_CONTENT_TYPE = "view_contenttype"
    ADD_CONTENT_TYPE = "add_contenttype"
    CHANGE_CONTENT_TYPE = "change_contenttype"
    DELETE_CONTENT_TYPE = "delete_contenttype"


class RolesAndPermissionsUrlsEnum(Enum):
    ROLE_PERMISSION_URL = reverse("permission_management_api:group-list")
    CONTENT_TYPE_LIST_URL = reverse("permission_management_api:contenttype-list")
    USER_PERMISSIONS_LIST_URL = reverse(
        "permission_management_api:user-permissions-list"
    )
    CONTENT_TYPE_DETAIL_URL = "permission_management_api:contenttype-detail"
    ROLE_PERMISSION_DETAIL_URL = "permission_management_api:group-detail"
    ROLE_PERMISSION_DETAIL_NAMESPACE = "user_api:role-permissions-detail"
    PERMISSION_LIST_URL = reverse("permission_management_api:permission-list")
    PERMISSION_DETAIL_URL = "permission_management_api:permission-detail"


REQUIRED_PERMISSIONS_TO_GET_ROLES = [
    PermissionsEnum.VIEW_GROUP,
    PermissionsEnum.VIEW_PERMISSION,
]
REQUIRED_PERMISSIONS_TO_POST_ROLES = [
    PermissionsEnum.ADD_GROUP,
    PermissionsEnum.ADD_PERMISSION,
]
REQUIRED_PERMISSIONS_TO_UPDATE_ROLES = [
    PermissionsEnum.CHANGE_GROUP,
    PermissionsEnum.ADD_PERMISSION,
    PermissionsEnum.CHANGE_PERMISSION,
]
REQUIRED_PERMISSIONS_TO_DELETE_ROLES = [
    PermissionsEnum.DELETE_GROUP,
    PermissionsEnum.DELETE_PERMISSION,
]
REQUIRED_PERMISSIONS_TO_GET_CONTENT_TYPES = [
    PermissionsEnum.VIEW_CONTENT_TYPE,
]
REQUIRED_PERMISSIONS_TO_GET_USER_PERMISSION = [
    PermissionsEnum.VIEW_PERMISSION,
]
REQUIRED_PERMISSIONS_TO_POST_PERMISSION = [
    PermissionsEnum.ADD_PERMISSION,
]
REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION = [
    PermissionsEnum.CHANGE_PERMISSION,
]
REQUIRED_PERMISSIONS_TO_DELETE_PERMISSION = [
    PermissionsEnum.DELETE_PERMISSION,
]

from random import randint

import pytest
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json

from permissions_management.api.serializers import (
    ContentTypeSerializer,
    PermissionSerializer,
)
from permissions_management.constants import (
    REQUIRED_PERMISSIONS_TO_DELETE_ROLES,
    REQUIRED_PERMISSIONS_TO_GET_ROLES,
    REQUIRED_PERMISSIONS_TO_POST_ROLES,
    REQUIRED_PERMISSIONS_TO_UPDATE_ROLES,
    REQUIRED_PERMISSIONS_TO_GET_CONTENT_TYPES,
    REQUIRED_PERMISSIONS_TO_GET_USER_PERMISSION,
    REQUIRED_PERMISSIONS_TO_POST_PERMISSION,
    REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION,
    REQUIRED_PERMISSIONS_TO_DELETE_PERMISSION,
    RolesAndPermissionsUrlsEnum,
    PermissionMessagesEnum,
)
from permissions_management.factories import GroupFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestRolePermissionViewSetList:
    def setup_method(self):
        self.api_client = APIClient()

    def test_role_permission_list_without_login(
        self,
    ):
        """Test case for role permission list api with unauthenticated user"""
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_role_permission_list_without_permissions(
        self,
    ):
        """Test case for role permission list api without permissions"""
        user = UserFactory()
        self.api_client.force_authenticate(user)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_list_with_only_view_group_perm(
        self,
    ):
        """Test case for role permission list api with only view_group permission"""
        user = UserFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_GET_ROLES[0].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_list_with_only_view_permission_perm(
        self,
    ):
        """Test case for role permission list api with only view_permission permission"""
        user = UserFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_GET_ROLES[1].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_list_success(self):
        """Test case for role permission list api with all requirements"""
        user = UserFactory()
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_GET_ROLES]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        roles_count = Group.objects.count()
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(result) == roles_count


class TestRolePermissionViewSetCreate:
    def setup_method(self):
        self.api_client = APIClient()

    def test_role_permission_create_without_login(
        self,
    ):
        """Test case for role permission create api with unauthenticated user"""
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_role_permission_create_with_only_add_group_perm(
        self,
    ):
        """Test case for role permission create api with only add_group permission"""
        user = UserFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_POST_ROLES[0].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_create_with_only_add_permission_perm(
        self,
    ):
        """Test case for role permission create api with only add_permission permission"""
        user = UserFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_POST_ROLES[1].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_user_role_create_view(self, user):
        """Test case for role permission create api with all requirements"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_POST_ROLES]
        )
        user.user_permissions.set(perms)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert result.get("name") == data.get("name")
        assert Group.objects.count() != 0

    def test_user_role_create_view_with_duplicate_name(self, user):
        """Test case for role permission create api with all requirements"""
        GroupFactory(name="Admin Group")
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_POST_ROLES]
        )
        user.user_permissions.set(perms)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert result.get("name") == ["group with this name already exists."]


class TestRolePermissionViewSetUpdate:
    def setup_method(self):
        self.api_client = APIClient()

    def test_role_permission_update_without_login_put_method(
        self,
    ):
        """Test case for role permission update api with unauthenticated user"""
        role = GroupFactory()
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_role_permission_update_without_login_patch_method(
        self,
    ):
        """Test case for role permission update api with unauthenticated user"""
        role = GroupFactory()
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_role_permission_update_object_does_not_exist_put_method(self, user):
        """Test case for role permission update api with wrong object id"""
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_ROLES]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        role = GroupFactory()
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id + 1},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert result.get("detail") == "Not found."

    def test_role_permission_delete_object_does_not_exist_patch_method(self, user):
        """Test case for role permission update api with wrong object id"""
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_ROLES]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        role = GroupFactory()
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id + 1},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert result.get("detail") == "Not found."

    def test_role_permission_delete_duplicate_name_not_allowed_put_method(self, user):
        """Test case for role permission update api with duplicate name"""
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_ROLES]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        role1 = GroupFactory(name="Quixom")
        role2 = GroupFactory(name="Admin Group")
        role2.user_set.add(user)
        data = {
            "name": role1.name,
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role2.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert result.get("name") == ["group with this name already exists."]

    def test_role_permission_delete_duplicate_name_not_allowed_patch_method(self, user):
        """Test case for role permission update api with duplicate name"""
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_ROLES]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        role1 = GroupFactory(name="Quixom")
        role2 = GroupFactory(name="Admin Group")
        role2.user_set.add(user)
        data = {
            "name": role1.name,
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role2.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert result.get("name") == ["group with this name already exists."]

    def test_role_permission_update_with_only_change_group_perm(self, user):
        """Test case for role permission update api with only change_group permission"""
        role = GroupFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_UPDATE_ROLES[0].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_update_with_only_add_permission_perm(self, user):
        """Test case for role permission update api with only add_permission permission"""
        role = GroupFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_UPDATE_ROLES[1].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_update_with_only_change_permission_perm(self, user):
        """Test case for role permission update api with only change_permission permission"""
        role = GroupFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_UPDATE_ROLES[2].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_update_with_add_permission_change_permission_perm(
        self, user
    ):
        """Test case for role permission update api with only change_permission permission"""
        role = GroupFactory()
        perms = Permission.objects.filter(
            codename__in=REQUIRED_PERMISSIONS_TO_UPDATE_ROLES[1:]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_update_with_add_permission_change_group_perm(self, user):
        """Test case for role permission update api with only change_permission permission"""
        role = GroupFactory()
        perms = Permission.objects.filter(
            codename__in=REQUIRED_PERMISSIONS_TO_UPDATE_ROLES[0:2]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_user_role_update_view_put_method_when_user_is_no_part_of_group(self, user):
        """Test case for role permission update api with all requirements"""
        role = GroupFactory()
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=REQUIRED_PERMISSIONS_TO_UPDATE_ROLES
        )
        user.user_permissions.set(perms)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_user_role_update_view_patch_method_when_user_is_no_part_of_group(
        self, user
    ):
        """Test case for role permission update api with all requirements"""
        role = GroupFactory()
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=REQUIRED_PERMISSIONS_TO_UPDATE_ROLES
        )
        user.user_permissions.set(perms)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_user_role_update_view_put_method(self, user):
        """Test case for role permission update api with all requirements"""
        role = GroupFactory()
        role.user_set.add(user)
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_ROLES]
        )
        user.user_permissions.set(perms)
        data = {
            "name": "Admin Group",
            "permissions": Permission.objects.all().values_list("id", flat=True),
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert result.get("name") == data.get("name")
        assert Group.objects.count() != 0

    def test_user_role_update_view_patch_method(self, user):
        """Test case for role permission update api with all requirements"""
        role = GroupFactory()
        role.user_set.add(user)
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_ROLES]
        )
        user.user_permissions.set(perms)
        data = {
            "name": "Admin Group",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert result.get("name") == data.get("name")
        assert Group.objects.count() != 0


class TestRolePermissionViewSetDelete:
    def setup_method(self):
        self.api_client = APIClient()

    def test_role_permission_delete_without_login(
        self,
    ):
        """Test case for role permission delete api with unauthenticated user"""
        role = GroupFactory()
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_role_permission_delete_object_does_not_exist(self, user):
        """Test case for role permission delete api with unauthenticated user"""
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_DELETE_ROLES]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        role = GroupFactory()
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id + 1},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert result.get("detail") == "Not found."

    def test_role_permission_create_with_only_delete_group_perm(self, user):
        """Test case for role permission delete api with only delete_group permission"""
        role = GroupFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_DELETE_ROLES[0].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_role_permission_create_with_only_delete_permission_perm(self, user):
        """Test case for role permission delete api with only delete_permission permission"""
        role = GroupFactory()
        perms = Permission.objects.filter(
            codename=REQUIRED_PERMISSIONS_TO_DELETE_ROLES[1].value
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_user_role_delete_view_when_user_is_not_part_of_group(self, user):
        """Test case for role permission delete api with all requirements"""
        role = GroupFactory()
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=REQUIRED_PERMISSIONS_TO_DELETE_ROLES
        )
        user.user_permissions.set(perms)
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            )
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        result = json.loads(response.content)
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_user_role_delete_view(self, user):
        """Test case for role permission delete api with all requirements"""
        role = GroupFactory()
        role.user_set.add(user)
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[value.value for value in REQUIRED_PERMISSIONS_TO_DELETE_ROLES]
        )
        user.user_permissions.set(perms)
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            )
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Group.objects.count() == 0


class TestContentTypeListView:
    def setup_method(self):
        self.api_client = APIClient()

    def test_list_content_type_without_login(self):
        """Test case for content_type list api with unauthenticated user"""
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.CONTENT_TYPE_LIST_URL.value
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_list_content_type_without_permissions(self, user):
        """Test case for content_type list api with unauthorised user"""
        self.api_client.force_authenticate(user)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.CONTENT_TYPE_LIST_URL.value
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_list_content_type_list_success(self, user):
        """Test case for content_type list api success"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_GET_CONTENT_TYPES
            ]
        )
        user.user_permissions.set(perms)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.CONTENT_TYPE_LIST_URL.value
        )
        result = json.loads(response.content)
        serializer_data = ContentTypeSerializer(
            ContentType.objects.all(), many=True
        ).data
        assert response.status_code == status.HTTP_200_OK
        assert len(result) == ContentType.objects.count()
        assert result == serializer_data

    def test_detail_content_type_without_login(self):
        """Test case for content_type detail api with unauthenticated user"""
        content_type = ContentType.objects.first()
        response = self.api_client.get(
            path=reverse(
                RolesAndPermissionsUrlsEnum.CONTENT_TYPE_DETAIL_URL.value,
                kwargs={"pk": content_type.id},
            )
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_detail_content_type_without_permissions(self, user):
        """Test case for content_type detail api with unauthorised user"""
        self.api_client.force_authenticate(user)
        content_type = ContentType.objects.first()
        response = self.api_client.get(
            path=reverse(
                RolesAndPermissionsUrlsEnum.CONTENT_TYPE_DETAIL_URL.value,
                kwargs={"pk": content_type.id},
            )
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_detail_content_type_not_found(self, user):
        """Test case for content_type detail api with incorrect pk"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_GET_CONTENT_TYPES
            ]
        )
        user.user_permissions.set(perms)
        response = self.api_client.get(
            path=reverse(
                RolesAndPermissionsUrlsEnum.CONTENT_TYPE_DETAIL_URL.value,
                kwargs={"pk": "%05d" % randint(9999, 99999)},
            )
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert result.get("detail") == "Not found."

    def test_content_type_detail_success(self, user):
        """Test case for content_type detail api success"""
        self.api_client.force_authenticate(user)
        content_type = ContentType.objects.first()
        permissions = PermissionSerializer(
            content_type.permission_set.all(), many=True
        ).data
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_GET_CONTENT_TYPES
            ]
        )
        user.user_permissions.set(perms)
        response = self.api_client.get(
            path=reverse(
                RolesAndPermissionsUrlsEnum.CONTENT_TYPE_DETAIL_URL.value,
                kwargs={"pk": content_type.id},
            )
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert result.get("name") == content_type.name
        assert result.get("permission_set") == permissions


class TestUserPermissionListView:
    def setup_method(self):
        self.api_client = APIClient()

    def test_permission_get_without_login(self):
        """test to check if permissions are listed with unauthenticated user"""

        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.USER_PERMISSIONS_LIST_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_permission_get_without_permissions(self, user):
        """test to check if permissions are listed with unauthorised user"""
        self.api_client.force_authenticate(user)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.USER_PERMISSIONS_LIST_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_permission_list_success(self, user):
        """test to check if permissions are listed successfully"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_GET_USER_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.USER_PERMISSIONS_LIST_URL.value,
            format="json",
        )
        result = json.loads(response.content)
        serializer_data = PermissionSerializer(
            user.user_permissions.all(), many=True
        ).data
        assert response.status_code == status.HTTP_200_OK
        assert result == serializer_data


class TestPagination:
    def setup_method(self):
        self.api_client = APIClient()
        self.url = reverse("permission_management_api:user-permissions-list")

    def test_pagination_enabled(self, user):
        """Send request with pagination enabled"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.all()
        perms_count = perms.count()
        user.user_permissions.set(perms)
        url = reverse("permission_management_api:user-permissions-list")
        response = self.api_client.get(url, {"pagination": "true"})
        result = json.loads(response.content)

        assert "count" in result
        assert "next" in result
        assert "previous" in result
        assert "results" in result
        assert len(result.get("results")) == 10  # Default page size
        assert result.get("count") == perms_count  # Default page size

    def test_pagination_disabled(self, user):
        """Send request without pagination"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.all()
        user.user_permissions.set(perms)
        response = self.api_client.get(self.url)
        result = json.loads(response.content)

        assert "count" not in result  # No pagination metadata
        assert "next" not in result
        assert "previous" not in result
        assert (
            len(result) == user.user_permissions.count()
        )  # returning the expected data

    def test_custom_page_size(self, user):
        """Send request with custom page size"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.all()
        user.user_permissions.set(perms)
        response = self.api_client.get(self.url, {"pagination": "true", "limit": 5})
        result = json.loads(response.content)

        assert len(result.get("results")) == 5  # Custom page size

    def test_wrong_value_for_pagination(self, user):
        """Invalid pagination parameter value"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.all()
        user.user_permissions.set(perms)
        response = self.api_client.get(self.url, {"pagination": "abc"})
        result = json.loads(response.content)

        assert "count" not in result  # No pagination metadata

        # Invalid page size parameter value
        response = self.api_client.get(
            self.url, {"pagination": "true", "page_size": -10}
        )
        result = json.loads(response.content)

        assert len(result.get("results")) == 10  # Default page size

    def test_opt_out_pagination(self, user):
        """Send request to opt-out of pagination"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.all()
        user.user_permissions.set(perms)
        response = self.api_client.get(self.url, {"pagination": "false"})
        assert "count" not in response.data  # No pagination metadata


class TestInstanceAndGroupLevelPermission:
    def setup_method(self):
        self.api_client = APIClient()

    def test_instance_access_without_group_permission(self, user):
        """test if the user is a?ble to access any url without being in ay group"""
        self.api_client.force_authenticate(user)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value, format="json"
        )
        result = json.loads(response.content)
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_instance_access_without_instance_permission(self, user):
        """test if the user is able to access any url without having any permissions"""
        self.api_client.force_authenticate(user)
        response = self.api_client.get(
            path=RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_URL.value, format="json"
        )
        result = json.loads(response.content)
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_instance_access_with_only_group_permission(self, user):
        """test if the user is able to access any url having group permissions"""
        self.api_client.force_authenticate(user)
        permissions = Permission.objects.filter(
            content_type__app_label="group"
        ).values_list("id", flat=True)
        role = GroupFactory(name="test_group")
        role.permissions.set(permissions)
        role.user_set.add(user)
        response = self.api_client.get(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_instance_access_with_only_instance_permission(self, user):
        """test if the user is able to access any url without only permissions"""
        role = GroupFactory()
        role.user_set.add(user)
        self.api_client.force_authenticate(user)
        permissions = Permission.objects.filter(codename__endswith="group")
        user.user_permissions.set(permissions)
        data = {
            "name": "Admin Group",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert result.get("name") == data.get("name")

    def test_instance_access_with_only_group_perm_as_well_as_with_only_instance_permissions(
        self,
    ):
        """test if the user is able to access any url with only permissions and with only instance permissions"""
        user_1 = UserFactory(username="junior HR")
        user_2 = UserFactory(username="senior HR")
        perms = Permission.objects.filter(codename__icontains="group")
        user_2.user_permissions.set(
            perms
        )  # assigning instance permissions to senior HR.
        role = GroupFactory(name="HR")
        role.permissions.set(perms)
        role.user_set.add(user_1)
        role.user_set.add(user_2)

        #  Junior HR requests change in existing group with no instance permissions to do so.
        self.api_client.force_authenticate(user_1)
        data = {
            "name": "Admin Group",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

        #  Senior HR requests change in existing group with all instance permissions to do so.
        self.api_client.force_authenticate(user_2)
        data = {
            "name": "Admin Group",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert result.get("name") == data.get("name")

    def test_instance_access_with_both_permissions(self, user):
        """test if the user is able to access any url with both permissions"""
        role = GroupFactory()
        role.user_set.add(user)
        self.api_client.force_authenticate(user)
        permissions = Permission.objects.filter(codename__endswith="group")
        user.user_permissions.set(permissions)
        data = {
            "name": "Admin Group",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.ROLE_PERMISSION_DETAIL_URL.value,
                kwargs={"pk": role.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert result.get("name") == data.get("name")


class TestPermissionViewSetCreate:
    def setup_method(self):
        self.api_client = APIClient()

    def test_permission_create_without_login(
        self,
    ):
        """Test case for role permission create api with unauthenticated user"""
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.PERMISSION_LIST_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_permission_create_without_permission(self, user):
        """Test case for role permission create api without permissions"""
        self.api_client.force_authenticate(user)
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.PERMISSION_LIST_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_permission_create_with_incorrect_content_type_id(self, user):
        """Test case for role permission create api with incorrect content_type id"""
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_POST_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "content_type_id": 1000,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.PERMISSION_LIST_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert result == ["ContentType matching query does not exist."]

    def test_permission_create_with_duplicate_codename(self, user):
        """Test case for role permission create api with duplicate codename"""
        permission = Permission.objects.first()
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_POST_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        data = {
            "content_type_id": permission.content_type.id,
            "name": permission.name,
            "codename": permission.codename,
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.PERMISSION_LIST_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert result.get("codename") == [
            "Duplicate codename. Please try different codename"
        ]

    def test_permission_create_view(self, user):
        """Test case for role permission create api with all requirements"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_POST_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.post(
            path=RolesAndPermissionsUrlsEnum.PERMISSION_LIST_URL.value,
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert result.get("codename") == data.get("codename")
        assert Permission.objects.filter(codename=result.get("codename"))


class TestPermissionViewSetUpdate:
    def setup_method(self):
        self.api_client = APIClient()
        self.permission = Permission.objects.create(
            content_type_id=1,
            name="can add custom permission",
            codename="add_custom_permission",
        )

    def test_permission_put_method_without_login(
        self,
    ):
        """Test case for role permission update api with unauthenticated user"""
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_permission_put_method_without_permission(self, user):
        """Test case for role permission update api with only add_group permission"""
        self.api_client.force_authenticate(user)
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_permission_put_method_with_incorrect_pk(self, user):
        """Test case for role permission update api with only add_permission permission"""
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "content_type_id": 1000,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": "%05d" % randint(999, 99999)},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert result.get("detail") == "Not found."

    def test_permission_put_method_with_duplicate_codename(self, user):
        """Test case for role permission update api with all requirements"""
        self.api_client.force_authenticate(user)
        permission = Permission.objects.last()
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        data = {
            "content_type_id": permission.content_type.id,
            "name": permission.name,
            "codename": permission.codename,
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert result.get("codename") == [
            "Duplicate codename. Please try different codename"
        ]

    def test_permission_put_method_view(self, user):
        """Test case for role permission update api with all requirements"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.put(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        self.permission.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert result.get("codename") == data.get("codename")
        assert (
            Permission.objects.filter(codename=data.get("codename")).first()
            == self.permission
        )

    def test_permission_patch_method_without_login(
        self,
    ):
        """Test case for role permission update api with unauthenticated user"""
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_permission_patch_method_without_permission(self, user):
        """Test case for role permission update api with only add_group permission"""
        self.api_client.force_authenticate(user)
        data = {
            "content_type_id": 1,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_permission_patch_method_with_incorrect_pk(self, user):
        """Test case for role permission update api with incorrect pk"""
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        data = {
            "content_type_id": 1000,
            "name": "can custom permission",
            "codename": "custom_permission",
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": "%05d" % randint(999, 99999)},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert result.get("detail") == "Not found."

    def test_permission_patch_method_with_duplicate_codename(self, user):
        """Test case for role permission update api with duplicate codename"""
        self.api_client.force_authenticate(user)
        permission = Permission.objects.last()
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        data = {
            "content_type_id": permission.content_type.id,
            "name": permission.name,
            "codename": permission.codename,
        }
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert result.get("codename") == [
            "Duplicate codename. Please try different codename"
        ]

    def test_permission_patch_method_view(self, user):
        """Test case for role permission update api with all requirements"""
        self.api_client.force_authenticate(user)
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_UPDATE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        data = {"codename": "custom_permission"}
        response = self.api_client.patch(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            data=data,
            format="json",
        )
        result = json.loads(response.content)
        self.permission.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert Permission.objects.filter(codename=result.get("codename"))
        assert (
            result.get("codename") == data.get("codename") == self.permission.codename
        )


class TestPermissionViewSetDelete:
    def setup_method(self):
        self.api_client = APIClient()
        self.permission = Permission.objects.first()

    def test_permission_delete_without_login(
        self,
    ):
        """Test case for role permission delete api with unauthenticated user"""
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert result.get("detail") == "Authentication credentials were not provided."

    def test_permission_delete_without_permission(self, user):
        """Test case for role permission delete api without permissions"""
        self.api_client.force_authenticate(user)
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            result.get("detail")
            == PermissionMessagesEnum.PERMISSION_DENIED_MESSAGE.value
        )

    def test_permission_delete_with_detail_not_found(self, user):
        """Test case for role permission delete api with detail not found"""
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_DELETE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": "%05d" % randint(9999, 99999)},
            ),
            format="json",
        )
        result = json.loads(response.content)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert result.get("detail") == "Not found."

    def test_permission_delete_view(self, user):
        """Test case for role permission delete api with all requirements"""
        perms = Permission.objects.filter(
            codename__in=[
                value.value for value in REQUIRED_PERMISSIONS_TO_DELETE_PERMISSION
            ]
        )
        user.user_permissions.set(perms)
        self.api_client.force_authenticate(user)
        response = self.api_client.delete(
            path=reverse(
                RolesAndPermissionsUrlsEnum.PERMISSION_DETAIL_URL.value,
                kwargs={"pk": self.permission.id},
            ),
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Permission.objects.filter(codename=self.permission.codename)

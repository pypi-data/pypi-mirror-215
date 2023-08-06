from django.urls import path
from rest_framework import routers

from permissions_management.api.views import (
    PermissionViewSet,
    GroupViewSet,
    ContentTypeViewSet,
    UserPermissionListView,
)

app_name = "permission_management_api"

router = routers.SimpleRouter()
router.register(r"groups", GroupViewSet)
router.register(r"content_types", ContentTypeViewSet)
router.register(r"permissions", PermissionViewSet)

urlpatterns = router.urls

urlpatterns += [
    path(
        "user/permissions/",
        UserPermissionListView.as_view(),
        name="user-permissions-list",
    )
]

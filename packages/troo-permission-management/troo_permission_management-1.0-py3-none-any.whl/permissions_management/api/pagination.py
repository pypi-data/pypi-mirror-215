import coreapi
import coreschema
from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    """class to paginate only when the query param represents pagination=true"""

    def get_schema_fields(self, view):
        schema_parameters = super().get_schema_fields(view)
        schema_parameters.append(
            coreapi.Field(
                name="pagination",
                required=False,
                location="query",
                schema=coreschema.Boolean(
                    title="Pagination",
                    description="If set to true, the queryset will be paginated; otherwise, it will not.",
                ),
            )
        )
        return schema_parameters

    def paginate_queryset(self, queryset, request, view=None):
        """method to paginate only when the query param represents pagination=true"""
        if request.GET.get("pagination", "").lower() != "true":
            return None  # Skip pagination

        return super().paginate_queryset(queryset, request, view)

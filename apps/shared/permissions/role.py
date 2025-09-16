from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    """
    DRF Has role permission class
    Example:
        class TestView(APIView):
            permission_classes = (HasRole([RoleChoices.ADMIN]),)
    """

    def __init__(self, roles: list) -> None:
        super().__init__()
        self.roles = roles

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role in self.roles)

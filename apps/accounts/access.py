from functools import wraps

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("Authentication is required.")
            if request.user.role not in allowed_roles:
                raise PermissionDenied("You do not have access to this page.")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


class RoleRequiredMixin(AccessMixin):
    allowed_roles = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in self.allowed_roles:
            raise PermissionDenied("You do not have access to this page.")
        return super().dispatch(request, *args, **kwargs)


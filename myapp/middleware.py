from threading import local
from django.utils.deprecation import MiddlewareMixin

_request_local = local()

def set_current_user(user):
    """Store the current Django user in thread-local storage."""
    _request_local.user = user

def get_current_user():
    """Retrieve the current Django user from thread-local storage."""
    return getattr(_request_local, "user", None)

class CurrentUserMiddleware(MiddlewareMixin):
    """Middleware to store the current user in thread-local storage for logging purposes."""

    def process_request(self, request):
        """Store the authenticated user in thread-local storage."""
        set_current_user(getattr(request, "user", None))

    def process_response(self, request, response):
        """Clear the stored user after the request is processed."""
        set_current_user(None)
        return response

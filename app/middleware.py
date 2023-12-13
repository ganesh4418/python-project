from django.utils import timezone


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Update last activity timestamp for authenticated users
            request.user.last_activity = timezone.now()
            request.user.save()

        return response
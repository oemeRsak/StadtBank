from Bank.models import Setting
from django.shortcuts import redirect
from django.urls import resolve


class SetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/static/'):
            return self.get_response(request)

        setup_completed = Setting.objects.filter(
            key="SETUP_COMPLETED", value={'value': True}).exists()

        # Allow access to the setup page or static files
        if resolve(request.path).url_name == "setup" or setup_completed:
            if resolve(request.path).url_name == "setup" and setup_completed:
                return redirect("Bank:index")
            return self.get_response(request)

        # Redirect non-setup requests to setup if setup is not completed
        return redirect("Bank:setup")

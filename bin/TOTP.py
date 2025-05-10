"""bin/TOTP.py"""
import time
import getpass

from django.http import HttpResponse, HttpResponseBadRequest
import django.core.exceptions

try:
    from django.contrib.auth.models import User
except django.core.exceptions.ImproperlyConfigured:
    pass


# curl -X POST -d "password=PASSWORD" 127.0.0.1/newPass

class TOTPError(Exception):
    pass


# You can customize it with your Super User Account
def newWorkerPassword(adminPass: str = "", httpRequest: bool = False):
    """Change Worker password. It will return the new Password"""
    if User.objects.filter(username='admin', is_superuser=True).exists():
        # If there is, prompt for the password
        if not adminPass:
            adminPass = input("Enter the password for the superuser 'admin': ")

        # Retrieve the user with the username "admin"
        admin_user = User.objects.get(username='admin')

        # Check if the provided password is correct
        if admin_user.check_password(adminPass):
            passw = str(int(time.time()))[-5:]
            user = User.objects.get(username="worker")
            user.set_password(passw)
            user.save(update_fields=["password"])

            if httpRequest:
                return HttpResponse(f"{passw}\n")
            else:
                return passw
        else:
            if httpRequest:
                # I dont Know is that the correct Error
                return HttpResponseBadRequest("Incorrect Password\n")
            else:
                raise TOTPError("Incorrect password for superuser 'admin'.")
    else:
        if httpRequest:
            # I dont Know is that the correct Error
            return HttpResponseBadRequest("No Admin Account")
        else:
            raise TOTPError("There is no superuser with the username 'admin'.")


if __name__ == "__main__":
    import os
    import sys

    import django
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'StadtBank.settings')
    django.setup()
    from django.contrib.auth.models import User

    try:
        new_password = newWorkerPassword(
            getpass.getpass("Enter Admin Password: "))
        print("New password for worker:", new_password)
    except TOTPError as e:
        print("Error:", e)

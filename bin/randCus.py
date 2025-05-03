"""bin/randCus.py"""
import os
import sys
from random import randint

import django
from faker import Faker

fake = Faker()


def randCus(stop: int = 0):
    """Create Random Customer Data."""
    for _ in range(randint(20, 30) if stop == 0 else stop):
        first_name = fake.first_name()
        last_name = fake.last_name()
        balance = randint(0, 100)

        Customer(name=f"{first_name} {last_name}", balance=balance).save()


if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'StadtBank.settings')
    django.setup()

    from Bank.models import Customer  # type: ignore
    randCus()

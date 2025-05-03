"""bin/randAct.py"""
import os
import sys
from datetime import datetime
from random import randint

import django
from faker import Faker


def randAct(stop: int = 0):
    """Create Random Action Data."""
    for _ in range(randint(20, 30) if stop == 0 else stop):
        action_type = randint(1, 3)

        
        CustomerCount = Customer.objects.count()
        if CustomerCount == 0:
            raise ValueError(
                "No customers found. Please create customers first.")


        customer = Customer.objects.get(
            nr=randint(1, CustomerCount))

        if action_type == 1:
            Action(customer=customer, type="payin",
                   amount=randint(1, 100), before=customer.balance).save()

        if action_type == 2:
            try:
                amount = randint(1, customer.balance)
                Action(customer=customer, type="payout",
                       amount=randint(1, customer.balance), before=customer.balance).save()
            except ValueError:
                pass

        if action_type == 3:
            related = Customer.objects.get(
                nr=randint(1, Customer.objects.count()))
            try:
                amount = randint(1, customer.balance)

                Action(customer=customer, related=related,
                       type="transfer", amount=amount).save()
            except ValueError:
                pass


if __name__ == "__main__":
    fake = Faker()
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'StadtBank.settings')
    django.setup()

    from Bank.models import Action, Customer  # type: ignore
    randAct()

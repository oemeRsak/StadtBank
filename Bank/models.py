"""Bank/models.py"""
from django.db import models


class Customer(models.Model):
    """Customer Class"""
    nr = models.IntegerField(
        primary_key=True, unique=True, auto_created=False)
    name = models.TextField()
    balance = models.IntegerField(default=0)
    credits = models.IntegerField(default=0, null=True)

    def __str__(self):
        """Customer.__str__"""
        return f"{self.name} | {self.nr}"

    class Meta:
        """Customer.Meta Class"""
        db_table = 'customers'


class Action(models.Model):
    """Action Class"""
    id = models.IntegerField(
        primary_key=True, auto_created=True)
    customer = models.ForeignKey(
        Customer, related_name="action_customer", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    type = models.TextField(choices=[('payin', 'Pay In'),
                                     ('payin-salary', 'Pay In (Salary)'),
                                     ('payout', 'Pay Out'),
                                     ('transfer', 'Transfer'),
                                     ('take-credit', 'Take Credit'),
                                     ('pay-credit', 'Pay Credit')])
    amount = models.IntegerField(null=True)
    related = models.ForeignKey(
        Customer, related_name="action_related", on_delete=models.CASCADE, null=True)
    before = models.IntegerField(null=True)

    def __str__(self):
        """Action.__str__"""
        return f"Action {self.id}"

    class Meta:
        """Action.Meta Class"""
        db_table = 'actions'


class Setting(models.Model):
    """Setting Class"""
    # Setting.objects.get(key="KEY").value['value']
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()

    def __str__(self):
        """Action.__str__"""
        return f"{self.key}"

    class Meta:
        """Setting.Meta Class"""
        db_table = 'settings'

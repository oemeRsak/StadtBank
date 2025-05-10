"""Django Modules"""
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import (Http404, HttpResponse,  # HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import url_has_allowed_host_and_scheme

from bin import TOTP  # type: ignore

from .forms import CreditF, CustomerF, PayF, TransferF, newCustomerF
from .models import Action, Customer, Setting

logger = logging.getLogger(__name__)


def index(request) -> HttpResponse:
    """Index Page"""

    return render(request, 'dashboard.html',
                  {'customers': Customer.objects.all(),
                   'actions': Action.objects.select_related('customer', 'related').all()})


class Customers(View):
    """Customers Page"""

    def get(self, request) -> HttpResponse:
        """Customers.get"""
        return render(request, 'customers.html', {'customers': Customer.objects.all()})


class CustomerDV(View):
    """Customer Detail View page"""

    def get(self, request, nr) -> HttpResponse:
        """CustomerDV.get"""
        try:
            customer = get_object_or_404(Customer, nr=nr)

            actions = Action.objects.filter(customer=nr).union(
                Action.objects.filter(related=nr))

            return render(request, 'customer.html', {'customer': customer, 'actions': actions})
        except Http404:
            return render(request, '404.html')


class Pay(View):
    """Pay Page"""
    customers = Customer.objects.all()

    def get(self, request) -> HttpResponse:
        """Pay.get"""
        return render(request, 'pay.html', {'customers': self.customers})


class CreditManagment(View):
    """Credit Page"""

    customers = Customer.objects.all()
    actions = Action.objects.all()

    def get(self, request) -> HttpResponse:
        """Credit.get"""
        return render(request, 'credit.html', {'customers': self.customers,
                                               'actions': self.actions})


# Not in Use
def pay_in(request) -> HttpResponseRedirect:
    """payIn API"""

    if request.method == "POST":
        form = CustomerF(request.POST)

        if form.is_valid():
            datas = form.cleaned_data
            target = Customer.objects.get(nr=datas["nr"])
            target.balance += datas["amount"]
            target.save()

            action = Action(
                nr=datas["nr"], actiontype="payin", amount=datas["amount"])
            action.save()

        else:
            print("NotValid")

    return HttpResponseRedirect("/.")


# Not in Use
def pay_out(request) -> HttpResponseRedirect:
    """PayOut API"""

    if request.method == "POST":
        form = CustomerF(request.POST)

        if form.is_valid():
            datas = form.cleaned_data
            target = Customer.objects.get(nr=datas["nr"])
            target.balance -= datas["amount"]
            target.save()

            action = Action(
                nr=datas["nr"], actiontype="payout", amount=datas["amount"])
            action.save()

        else:
            print("NotValid")

    return HttpResponseRedirect("/.")


@login_required
def pay(request):
    """Pay API"""
    if request.method == "POST":

        # Calculating Hour Salary before Form validation.
        if 'isSalary' in locals()['request'].POST and request.POST['isSalary'] == 'on':
            request.POST._mutable = True  # pylint: disable=protected-access
            if request.POST["payAmount"].lower().endswith("h"):
                hourSalary = Setting.objects.get(
                    key="hourSalary").value['value']
                # I know that is no the right way to do this. But anyway
                request.POST["payAmount"] = hourSalary * \
                    int(request.POST["payAmount"][:-1])
            request.POST["payType"] = "payin-salary"

        form = PayF(request.POST)
        if form.is_valid():
            payType = request.POST.get("payType")
            if payType in ('payin', 'payin-salary'):
                datas = form.cleaned_data
                target = datas["customer"]

                before = target.balance

                target.balance += datas["payAmount"]
                target.save()

            elif payType == "payout":
                datas = form.cleaned_data
                target = datas["customer"]
                before = target.balance
                target.balance -= datas["payAmount"]
                target.save()

            else:
                return HttpResponse(status=500)

            Action(customer=datas["customer"], type=payType,
                   amount=datas["payAmount"], before=before).save()

    return HttpResponseRedirect("/pay")


def transfer(request) -> HttpResponseRedirect:
    """Transfer API"""
    if request.method == "POST":
        form = TransferF(request.POST)

        if form.is_valid():
            datas = form.cleaned_data
            customer = datas["nr"]
            customer1 = datas["related"]
            amount = datas["amount"]
            customer.balance -= amount
            customer1.balance += amount
            customer.save()
            customer1.save()

            action = Action(
                customer=datas["nr"],
                related=datas["related"],
                type="transfer",
                amount=datas["amount"]
            )
            action.save()

    return HttpResponseRedirect("/pay")


@login_required
def newCustomer(request) -> HttpResponseRedirect:
    """NewCustomer API"""
    if request.method == "POST":
        form = newCustomerF(request.POST)

        if form.is_valid():
            datas = form.cleaned_data
            customer = Customer(name=datas["name"])

            customer.save()
    return HttpResponseRedirect("/customers")


@login_required
def credit(request) -> HttpResponseRedirect:
    """Crediy API"""
    if request.method == "POST":
        form = CreditF(request.POST)
        if form.is_valid():
            datas = form.cleaned_data
            target = datas["customer"]
            amount = datas["amount"]
            if request.POST["type"] == "take-credit":
                target.credits = target.credits + amount
            elif request.POST["type"] == "pay-credit":
                target.credits = target.credits - amount

            target.save()
            Action(customer=target,
                   type=request.POST["type"], amount=amount).save()

    return HttpResponseRedirect("/creditManagment")


class Login(View):
    """Login Page"""

    def get(self, request):
        """Login.get"""
        return render(request, 'login.html',
                      {'next': request.GET["next"]} if "next" in request.GET else None)

    def post(self, request):
        """Login.post"""
        logger.debug("Requested Login")
        passw = request.POST["passw"]
        user = authenticate(request, username="worker", password=passw)
        if user is not None:
            login(request, user)

        if request.GET.get('next') and \
                url_has_allowed_host_and_scheme(request.GET.get('next'),
                                                allowed_hosts=request.get_host()):
            return HttpResponseRedirect(request.GET["next"])

        return redirect('/')


@csrf_exempt
def newWorkerPass(request):
    """New Worker Password API"""
    if request.method == "POST":
        logger.debug("Requested new Worker Password from IP '%s', User-Agent '%s'",
                     request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT'])
        passw = TOTP.newWorkerPassword(
            request.POST['password'], httpRequest=True)
        return HttpResponse(passw, status=passw.status_code
                            if hasattr(locals()['passw'], 'status_code') else 200)
        # passw.status_code if 'passw.status_code' in locals() else 200)
    logger.critical("FALSE request for new Worker Password from '%s' (%s)",
                    request.META['REMOTE_ADDR'], request.META['HTTP_USER_AGENT'])

    return HttpResponseRedirect("/")

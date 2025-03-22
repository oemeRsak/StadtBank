"""Bank/urls.py"""
from django.urls import path

from . import views

app_name = "Bank"
urlpatterns = [
    path("", views.index, name="index"),
    path("customers/", views.Customers.as_view()),
    path("customers/<int:nr>", views.CustomerDV.as_view()),
    path("pay", views.Pay.as_view(), name="Pay In/Out"),
    path("paying", views.pay, name="pay"),
    path("newCustomer", views.newCustomer, name="newCustomer"),
    path("transfer", views.transfer, name="transfer"),
    path("creditManagment", views.CreditManagment.as_view(), name="Credit System"),
    path("credit", views.credit, name="credit"),
    path("login", views.Login.as_view(), name="login"),
    path("setup", views.FirstTimeSetup.as_view(), name="setup"),
    path("newPass", views.newWorkerPass, name="newWorkerPass")
]

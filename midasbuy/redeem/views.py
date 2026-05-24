from django.shortcuts import render
from accounts.models import MidasbuyAccount


def index(request):
    accounts = MidasbuyAccount.objects.filter(status=1)  # logged-in accounts only
    return render(request, "redeem/index.html", {"accounts": accounts})

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Client, Account

# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):
    usr = request.user
    client = Client.objects.get(clientid=usr)
    accts = Account.objects.filter(clientid__clientid=usr)
    posns = ...
    context = {
        'client': client,
        'accounts':accts
    }
    return render(request,"singleclient/index.html", context=context)

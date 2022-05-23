from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def index(request):
    # messages.success(request, "Good Morning David!!")
    # messages.warning(request, "So so Morning David!!")
    # messages.error(request, "Bad Morning David!!")
    return render(request,"singleclient/index.html")

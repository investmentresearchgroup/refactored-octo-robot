from django.shortcuts import render
from .models import Price
import pandas as pd

# Create your views here.
def display_data(request):
    query = Price.objects.all().values()
    frame = pd.DataFrame(query)
    context = {'frame': frame.to_html() }
    return render(request,'Ticker/main.html',context)

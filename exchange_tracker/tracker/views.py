from django.shortcuts import render
from .models import CountryIndex, IndexPrice, Ticker
from datetime import datetime

# Create your views here.


def index(request):
    indexprices = IndexPrice.objects.all().order_by('date')
    gse = CountryIndex.objects.filter(name='GSE')[0]
    tickers = Ticker.objects.all()
    context = {
        'indexprices': indexprices,
        'description': gse.description,
        'tickers': tickers,
    }
    return render(request, 'tracker/index.html', context)


def contact_us(request):
    return render(request, 'contact.html')


def single(request, pk):
    ticker = Ticker.objects.filter(id=pk).values()
    print(ticker)
    context = {
        'ticker': ticker
    }
    return render(request, 'tracker/single.html', context)

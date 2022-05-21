from django.shortcuts import redirect, render
from .models import CountryIndex, IndexPrice, Ticker
from django.contrib import messages
import datetime

# Create your views here.


def index(request):
    start = datetime.date(2011, 11, 5)
    indexprices = IndexPrice.objects.filter(date__gte=start).order_by('date')
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
    ticker = Ticker.objects.get(id=pk)
    context = {
        'ticker': ticker
    }
    return render(request, 'tracker/single.html', context)


def single_search(request):
    if "query" in request.GET:
        query = request.GET['query']
        ticker = Ticker.objects.filter(name=query)
        if not ticker.exists():
            messages.error(
                request, f"Ticker: {query} not found. Please enter a valid ticker name.")
    context = {
        'ticker': ticker
    }
    return render(request, 'tracker/single.html', context=context)

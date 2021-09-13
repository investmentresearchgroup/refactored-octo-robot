from django.shortcuts import render
from .models import CountryIndex, IndexPrice

# Create your views here.


def index(request):
    indexprices = IndexPrice.objects.all().order_by('date')
    gse = CountryIndex.objects.filter(name='GSE')[0]
    context = {
        'indexprices': indexprices,
        'description': gse.description
    }
    return render(request, 'tracker/index.html', context)


def contact_us(request):
    return render(request, 'contact.html')


def single(request):
    context = {
        'tickers': 'tickers'
    }
    return render(request, 'tracker/single.html', context)

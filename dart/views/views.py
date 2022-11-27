from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Amounts, Stocks
from ..serializers import StocksSerializer
from ..forms import SearchForm, AccountFilterForm, QuarterFilterForm, RatioFilterForm
from ..api.dart_filter import Filter

def index(request):
    # Test index.html
    return render(request, "index.html")

def search(request):
    form = SearchForm()
    
    if request.GET:
        stock_code = request.GET["stock_code"]
        stock_code = str(stock_code) + '.KS'
        try:
            amounts = Amounts.objects.filter(stock_code=stock_code)
        except Amounts.DoesNotExist:
            raise Http404("Amounts does not exist")
    else:
        stock_code = None
        amounts = None
    
    context = {
        'form': form,
        'stock_code': stock_code,
        'amounts': amounts,
    }
    
    return render(request, 'dart/search.html', context)
    
def detail(request, stock_code):
    if len(stock_code) == 6:
        stock_code = stock_code + '.KS'
    else:
        pass
        
    try:
        amounts = Amounts.objects.filter(stock_code=stock_code)
        stock_name = Stocks.objects.filter(stock_code=stock_code).values_list('stock_name', flat=True)[0]
    except Amounts.DoesNotExist:
        raise Http404("Amounts does not exist")
    
    context = {
        'stock_code': stock_code,
        'amounts': amounts,
        'stock_name': stock_name,
    }
    return render(request, 'dart/detail.html', context)

def detail_all(request, stock_code):
    if len(stock_code) == 6:
        stock_code = stock_code + '.KS'
    else:
        pass
        
    try:
        amounts = Amounts.objects.filter(stock_code=stock_code)
        amounts = str(list(amounts.values()))
        stock_name = Stocks.objects.filter(stock_code=stock_code).values_list('stock_name', flat=True)[0]
    except Amounts.DoesNotExist:
        raise Http404("Amounts does not exist")

    context = {
        'stock_code': stock_code,
        'amounts': amounts,
        'stock_name': stock_name,
    }
    return render(request, 'dart/detail_all.html', context)
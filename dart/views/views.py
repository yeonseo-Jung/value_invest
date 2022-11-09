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

class FilterView:

    def __init__(self):
        self.dartf = Filter()
        self.init_filter()
        
    def init_filter(self):
        self.dartf.init_quarters()
        self.dartf.init_amounts()
        self.dartf.init_ratios()
        self.dartf.init_codes()
        
        self.context = {}
    
    def _filter(self, request):
        ''' filter view function '''
        
        # Form
        quarter_form = QuarterFilterForm(request.POST or None)
        account_form = AccountFilterForm(None)
        ratio_form = RatioFilterForm(None)
        
        # context data
        context = {
            'quarter_form': quarter_form,
            'account_form': account_form,
            'ratio_form': ratio_form,
        }
        
        if request.POST:
            print('\n\n', request.POST, '\n\n')
            req_post_dict = request.POST.dict()
            
            # quarters
            if quarter_form.is_valid():
                quarters_idx = quarter_form.cleaned_data.get("quarter_field")
        
                quarters = []
                for idx in quarters_idx:
                    quarter = quarter_form.quarters_dict[idx]
                    quarters.append(quarter)
                
                self.dartf.quarters = quarters
            
                # accounts
                if 'account_field' in req_post_dict.keys():
                    account_idx = request.POST["account_field"]
                    account = account_form.accounts_dict[account_idx]
                    min_amount = request.POST["min_amount"].strip()
                    max_amount = request.POST["max_amount"].strip()
                    
                    # status check
                    min_amount, max_amount, status = self.preprocessor(min_amount, max_amount)
                    if status:
                        # filtering accounts amounts
                        self.dartf.amounts[account] = [min_amount, max_amount]
                        self.dartf.filter_amounts()
                    else:
                        pass
                    
                # ratios
                if 'ratio_field' in req_post_dict.keys():
                    ratio_idx = request.POST["ratio_field"]
                    ratio = ratio_form.ratios_dict[ratio_idx]
                    min_ratio = request.POST["min_ratio"].strip()
                    max_ratio = request.POST["max_ratio"].strip()
                    
                    # status check
                    min_ratio, max_ratio, status = self.preprocessor(min_ratio, max_ratio)
                    if status:
                        # filtering ratios
                        self.dartf.ratios[ratio] = [min_ratio, max_ratio]
                        self.dartf.filter_ratios()
                    else:
                        pass
                
            # # init filter
            # if len(req_post_dict.keys()) == 1:
            #     self.init_filter()

            # context data
            context['amounts'] = self.dartf.amounts
            context['ratios'] = self.dartf.ratios
            
            # intersect stock codes
            self.dartf.intersect()
            stock_codes_filterd = self.dartf.codes_filtered
            stocks = Stocks.objects.filter(stock_code__in=stock_codes_filterd)
            context['stock_codes'] = stock_codes_filterd
            context['stocks'] = stocks
            
        elif request.GET:
            self.init_filter()
            
        return render(request, 'dart/filter.html', context)

    def preprocessor(self, min_amount, max_amount):
        ''' min max amount preprocess '''
        
        if min_amount == '' and max_amount == '':
            min_amount, max_amount = None, None
            status = False
        elif min_amount == '':
            min_amount = None
            max_amount, status = self.dartf.conv_str(max_amount)
        elif max_amount == '':
            max_amount = None
            min_amount, status = self.dartf.conv_str(min_amount)
        else:
            min_amount, status = self.dartf.conv_str(min_amount)
            max_amount, status = self.dartf.conv_str(max_amount)
            try:
                if max_amount > min_amount:
                    status = True
                else:
                    pass
            except TypeError:
                status = False
        
        return min_amount, max_amount, status
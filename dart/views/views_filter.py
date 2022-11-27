from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse

from ..models import Amounts, Stocks
from ..serializers import StocksSerializer
from ..forms import SearchForm, AccountFilterForm, QuarterFilterForm, RatioFilterForm
from ..api.dart_filter import Filter
    
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View


# class based views sample
# class MyFormView(View):
#     form_class = AccountFilterForm
#     initial = {'key': 'value'}
#     template_name = 'form_template.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')

#         return render(request, self.template_name, {'form': form})

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
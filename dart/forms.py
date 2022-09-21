from email.policy import default
from django import forms
from .api.database import AccessDataBase

db_dart = AccessDataBase('root', 'jys1013011!', 'dart')

class SearchForm(forms.Form):
    stock_code = forms.CharField()

# YEARS = ('Y202111011', 'Y202011011', 'Y201911011', 'Y201811011')
    
class QuarterFilterForm(forms.Form):
    quarters = ['Q202211013', 
                'Q202111011', 'Q202111014', 'Q202111012', 'Q202111013',
                'Q202011011', 'Q202011014', 'Q202011012', 'Q202011013',
                'Q201911011', 'Q201911014', 'Q201911012', 'Q201911013',
                'Q201811011', 'Q201811014', 'Q201811012', 'Q201811013',]
    QUARTERS = []
    quarters_dict = {}
    i = 1
    for quarter in quarters:
        QUARTERS.append((str(i), quarter))
        quarters_dict[str(i)] = quarter
        i += 1
    quarter_field = forms.MultipleChoiceField(
        choices = QUARTERS,
        widget = forms.CheckboxSelectMultiple,
    )

class AccountFilterForm(forms.Form):
    conn, curs = db_dart._connect()
    query = f'SELECT DISTINCT(`account_nm_kor`) FROM `dart_accounts`;'
    curs.execute(query)
    data = curs.fetchall()
    curs.close()
    conn.close()
    
    accounts = [d['account_nm_kor'] for d in data]
    ACCOUNTS = []
    accounts_dict = {}
    i = 1
    for account in accounts:
        ACCOUNTS.append((str(i), account))
        accounts_dict[str(i)] = account
        i += 1
    ACCOUNTS = tuple(ACCOUNTS)
    
    account_field = forms.ChoiceField(choices=ACCOUNTS)
    min_amount = forms.CharField(required=False)
    max_amount = forms.CharField(required=False)
    
class RatioFilterForm(forms.Form):
    conn, curs = db_dart._connect()
    query = f'SELECT DISTINCT(`ratio`) FROM `dart_ratios`;'
    curs.execute(query)
    data = curs.fetchall()
    curs.close()
    conn.close()
    
    ratios = [d['ratio'] for d in data]
    RATIOS = []
    ratios_dict = {}
    i = 1
    for ratio in ratios:
        RATIOS.append((str(i), ratio))
        ratios_dict[str(i)] = ratio
        i += 1
    RATIOS = tuple(RATIOS)
    ratio_field = forms.ChoiceField(choices=RATIOS)
    min_ratio = forms.CharField(required=False, initial=None)
    max_ratio = forms.CharField(required=False)
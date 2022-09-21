import os
import sys
import collections
import pandas as pd

from .database import AccessDataBase

db = AccessDataBase('root', 'jys1013011!', 'dart')
class Filter:
    def __init__(self):
        self.init_amounts()
        self.init_ratios()
        self.init_codes()
        self.init_quarters()
        
    def init_amounts(self):
        self.amounts = {}
        self.dart_amounts = db.get_tbl('dart_amounts')
    
    def init_ratios(self):
        self.ratios = {}
        self.dart_ratios = db.get_tbl('dart_ratios')
        
    def init_codes(self):
        self.codes_amount = None
        self.codes_ratio = None
        self.codes_filtered = []
    
    def init_quarters(self):
        self.quarters = []

    def filter_amounts(self):
        
        columns = ['stock_code'] + self.quarters
        stock_codes = None
        dart_amounts_filtered = self.dart_amounts.copy()
        for account in self.amounts.keys():

            _amount = self.amounts[account]
            min_amount = _amount[0]
            max_amount = _amount[1]
            
            df_amounts_acc = dart_amounts_filtered.loc[dart_amounts_filtered.account_nm_kor==account, columns].reset_index(drop=True)

            for quarter in self.quarters:
                if min_amount is None:
                    stock_codes = df_amounts_acc.loc[df_amounts_acc[quarter]<=max_amount, 'stock_code'].tolist()
                elif max_amount is None:
                    stock_codes = df_amounts_acc.loc[df_amounts_acc[quarter]>=min_amount, 'stock_code'].tolist()
                else:    
                    stock_codes = df_amounts_acc.loc[(df_amounts_acc[quarter]>=min_amount) & (df_amounts_acc[quarter]<=max_amount), 'stock_code'].tolist()    
                
                df_amounts_acc = df_amounts_acc[df_amounts_acc.stock_code.isin(stock_codes)].reset_index(drop=True)
            
            print(f'{account}: {len(stock_codes)}')
            dart_amounts_filtered = dart_amounts_filtered[dart_amounts_filtered.stock_code.isin(stock_codes)].reset_index(drop=True)
            
        self.codes_amount = dart_amounts_filtered.stock_code.unique().tolist()
        print(f'Filtered stock codes (amounts): {len(self.codes_amount)}')
    
    def filter_ratios(self):
        
        columns = ['stock_code'] + self.quarters
        stock_codes = None
        dart_ratios_filtered = self.dart_ratios.copy()
        for ratio in self.ratios.keys():
            
            _ratio = self.ratios[ratio]
            min_ratio = _ratio[0]
            max_ratio = _ratio[1]
            
            df_ratios_acc = dart_ratios_filtered.loc[dart_ratios_filtered['ratio']==ratio, columns].reset_index(drop=True)
            for quarter in self.quarters:
                if min_ratio is None:
                    stock_codes = df_ratios_acc.loc[df_ratios_acc[quarter]<=max_ratio, 'stock_code'].tolist()
                elif max_ratio is None:
                    stock_codes = df_ratios_acc.loc[df_ratios_acc[quarter]>=min_ratio, 'stock_code'].tolist()
                else:    
                    stock_codes = df_ratios_acc.loc[(df_ratios_acc[quarter]>=min_ratio) & (df_ratios_acc[quarter]<=max_ratio), 'stock_code'].tolist()    
                
                df_ratios_acc = df_ratios_acc[df_ratios_acc.stock_code.isin(stock_codes)].reset_index(drop=True)

            print(f'{ratio}: {len(stock_codes)}')
            dart_ratios_filtered = dart_ratios_filtered[dart_ratios_filtered.stock_code.isin(stock_codes)].reset_index(drop=True)
            
        self.codes_ratio = dart_ratios_filtered.stock_code.unique().tolist()
        print(f'Filtered stock codes (ratios): {len(self.codes_ratio)}')
        
    def intersect(self):
        if self.codes_amount is None and self.codes_ratio is None:
            # require msg box
            self.codes_filtered = []
        elif self.codes_amount is None:
            self.codes_filtered = self.codes_ratio
        elif self.codes_ratio is None:
            self.codes_filtered = self.codes_amount
        elif len(self.codes_amount) == 0 or len(self.codes_ratio) == 0:
            self.codes_filtered = []
        else:
            stock_codes = self.codes_amount + self.codes_ratio
            self.codes_filtered = [item for item, count in collections.Counter(stock_codes).items() if count == 2]
    
    def conv_str(self, string):
        status = True
        flt = None
        try:
            flt = float(string)
        except ValueError:
            status = False
        return flt, status
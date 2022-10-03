from django.db import models

class Stocks(models.Model):
    stock_code = models.CharField(max_length=20)
    stock_name = models.CharField(max_length=255)

class Amounts(models.Model):
    # id = models.AutoField(primary_key=True)
    account_nm_eng = models.CharField(max_length=255)
    account_id = models.CharField(max_length=255)
    account_nm_kor = models.CharField(max_length=255)
    stock_code = models.CharField(max_length=20)
    fs_div = models.CharField(max_length=20)
    sj_div = models.CharField(max_length=20)
    # 2022
    Q202211013 = models.FloatField(null=True, blank=True, default=None)
    # 2021
    Q202111011 = models.FloatField(null=True, blank=True, default=None)
    Q202111014 = models.FloatField(null=True, blank=True, default=None)
    Q202111012 = models.FloatField(null=True, blank=True, default=None)
    Q202111013 = models.FloatField(null=True, blank=True, default=None)
    # 2020
    Q202011011 = models.FloatField(null=True, blank=True, default=None)
    Q202011014 = models.FloatField(null=True, blank=True, default=None)
    Q202011012 = models.FloatField(null=True, blank=True, default=None)
    Q202011013 = models.FloatField(null=True, blank=True, default=None)
    # 2019
    Q201911011 = models.FloatField(null=True, blank=True, default=None)
    Q201911014 = models.FloatField(null=True, blank=True, default=None)
    Q201911012 = models.FloatField(null=True, blank=True, default=None)
    Q201911013 = models.FloatField(null=True, blank=True, default=None)
    # 2018
    Q201811011 = models.FloatField(null=True, blank=True, default=None)
    Q201811014 = models.FloatField(null=True, blank=True, default=None)
    Q201811012 = models.FloatField(null=True, blank=True, default=None)
    Q201811013 = models.FloatField(null=True, blank=True, default=None)
    
class Accounts(models.Model):
    # id = models.AutoField(primary_key=True)
    account_nm_eng = models.CharField(max_length=255)
    account_id = models.CharField(max_length=255)
    account_nm_kor = models.CharField(max_length=255)
    
class Ratios(models.Model):
    # id = models.AutoField(primary_key=True)
    stock_code = models.CharField(max_length=20)
    ratio = models.CharField(max_length=255)
    # 2022
    Q202211013 = models.FloatField(null=True, blank=True, default=None)
    # 2021
    Q202111011 = models.FloatField(null=True, blank=True, default=None)
    Q202111014 = models.FloatField(null=True, blank=True, default=None)
    Q202111012 = models.FloatField(null=True, blank=True, default=None)
    Q202111013 = models.FloatField(null=True, blank=True, default=None)
    # 2020
    Q202011011 = models.FloatField(null=True, blank=True, default=None)
    Q202011014 = models.FloatField(null=True, blank=True, default=None)
    Q202011012 = models.FloatField(null=True, blank=True, default=None)
    Q202011013 = models.FloatField(null=True, blank=True, default=None)
    # 2019
    Q201911011 = models.FloatField(null=True, blank=True, default=None)
    Q201911014 = models.FloatField(null=True, blank=True, default=None)
    Q201911012 = models.FloatField(null=True, blank=True, default=None)
    Q201911013 = models.FloatField(null=True, blank=True, default=None)
    # 2018
    Q201811011 = models.FloatField(null=True, blank=True, default=None)
    Q201811014 = models.FloatField(null=True, blank=True, default=None)
    Q201811012 = models.FloatField(null=True, blank=True, default=None)
    Q201811013 = models.FloatField(null=True, blank=True, default=None)
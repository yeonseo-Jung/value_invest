from django.urls import path, include
from rest_framework import urls

from .views.views import search, detail, detail_all, index
from .views.views_user import RegisterApi
from .views.views_filter import FilterView

app_name = 'dart'
urlpatterns = [
    # /dart
    path('index/', index, name='index'),
    path('user/register', RegisterApi.as_view(), name='register'),
    path('search/', search, name='search'),
    path('filter/', FilterView()._filter, name='filter'),
    path('<str:stock_code>/', detail, name='detail'),
    path('<str:stock_code>/all/', detail_all, name='detail_all'),
]
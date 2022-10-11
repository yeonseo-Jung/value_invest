from django.urls import path

from .views import search, detail, detail_all, FilterView, index

app_name = 'dart'
urlpatterns = [
    # /dart
    path('index/', index, name='index'),
    path('search/', search, name='search'),
    path('filter/', FilterView()._filter, name='filter'),
    path('<str:stock_code>/', detail, name='detail'),
    path('<str:stock_code>/all/', detail_all, name='detail_all'),
]
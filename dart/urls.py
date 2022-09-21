from django.urls import path

from .views import search, detail, FilterView

app_name = 'dart'
urlpatterns = [
    # /dart
    path('search/', search, name='search'),
    path('filter/', FilterView()._filter, name='filter'),
    path('<str:stock_code>/', detail, name='detail'),
]
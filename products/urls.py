from django.urls import path
from .views import (Products, OneProduct)


urlpatterns = [
    path('', Products.as_view(), name='products'),
    path('<int:pk>', OneProduct.as_view(), name='OneProduct'),
]

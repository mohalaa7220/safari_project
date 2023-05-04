from django.urls import path
from .views import (Products, OneProduct, BarcodeScanView, QRCodeView
                    )


urlpatterns = [
    path('', Products.as_view(), name='products'),
    path('<int:pk>', OneProduct.as_view(), name='OneProduct'),
    path('barcode_scan/', BarcodeScanView.as_view()),
    path('<int:pk>/qr_code', QRCodeView.as_view(), name='qr_code'),
]

from rest_framework import status, generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import (AddProductSerializer,
                          UpdateProductSerializer, ProductSerializer)
from .models import Product
from .cursorPagination import ProductsPagination
from django_filters import rest_framework as filters
from .ProductFilter import ProductFilter
from io import BytesIO
from PIL import Image
import qrcode
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from project.serializer_error import serializer_error


def generate_qr_code(product):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(product.pk)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img


def save_qr_code(product):
    img = generate_qr_code(product)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    product.qr_code.save(f'{product.pk}.png', ContentFile(buffer.getvalue()))


class Products(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ProductsPagination
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter
    queryset = Product.objects.select_related('added_by', 'employee').all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def post(self, request, *args, **kwargs):
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            save_qr_code(serializer.instance)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Product Created Successfully"}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return serializer_error(serializer)


class OneProduct(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('added_by', 'employee').all()

    def update(self, request, pk=None):
        product = self.get_object()
        serializer = UpdateProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)
        else:
            return serializer_error(serializer)

    def delete(self, request, pk=None):
        product = self.get_object()
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)


# =========================

# =========================

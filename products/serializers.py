from rest_framework import serializers
from .models import Product, Employee


class AddProductSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.select_related('user').all())

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price', 'employee', 'image']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class UpdateProductSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.select_related('user').all())

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price', 'employee', 'image']

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'in_stock',
                  'price', 'employee', 'qr_code_url', 'image']

    def get_employee(self, obj):
        return f'{obj.employee.user.first_name} {obj.employee.user.last_name}'

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.qr_code.url)
        return None

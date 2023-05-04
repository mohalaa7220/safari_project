from rest_framework import serializers
from .models import Product, User


class AddProductSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price',
                  'employee', 'image', 'description']

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError(
                {"message": "Name of Product is required."})
        if not data.get('quantity'):
            raise serializers.ValidationError(
                {"message": "quantity is required."})

        if not data.get('price'):
            raise serializers.ValidationError(
                {"message": "price is required."})

        if not data.get('description'):
            raise serializers.ValidationError(
                {"message": "description is required."})

        # Check for empty values
        if data['name'] == '' or data['quantity'] == '' or data['price'] == '' or data['description'] == '':
            raise serializers.ValidationError(
                {"message": "Fields cannot be empty."})

        return data

    def create(self, validated_data):
        return Product.objects.create(**validated_data)


class UpdateProductSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'quantity', 'price',
                  'employee', 'image', 'description']

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError(
                {"message": "Name of Product is required."})
        if not data.get('quantity'):
            raise serializers.ValidationError(
                {"message": "quantity is required."})

        if not data.get('price'):
            raise serializers.ValidationError(
                {"message": "price is required."})

        if not data.get('description'):
            raise serializers.ValidationError(
                {"message": "description is required."})

        # Check for empty values
        if data['name'] == '' or data['quantity'] == '' or data['price'] == '' or data['description'] == '':
            raise serializers.ValidationError(
                {"message": "Fields cannot be empty."})

        return data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ProductSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()
    added_by = serializers.SerializerMethodField()
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'in_stock', 'added_by',
                  'price', 'employee', 'qr_code_url', 'image', 'description']

    def get_added_by(self, obj):
        return f'{obj.added_by.first_name} {obj.added_by.last_name}'

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.qr_code.url)
        return None

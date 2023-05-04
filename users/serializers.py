from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User, Manager, Employee
from django.db import transaction
from rest_framework.validators import UniqueValidator


# SignUp Manager
class SignUpManagerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email has already been used")])

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "password"]

    extra_kwargs = {
        'email': {'required': True},
        'phone': {'required': True},
        'password': {'required': True},
    }

    def validate(self, attrs):
        phone_exists = User.objects.filter(phone=attrs["phone"]).exists()
        if phone_exists:
            raise ValidationError({"message": "Phone has already been used"})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data['role'] = 'manager'
        user = User.objects.create_user(**validated_data, password=password)
        Manager.objects.create(user=user)
        return user


# SignUp Employee
class SignUpEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email has already been used")])

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone",
                  'password', 'status', 'shift_time', 'date_hired']

    extra_kwargs = {
        'email': {'required': True},
        'phone': {'required': True},
        'password': {'required': True},
    }

    def validate(self, attrs):
        phone_exists = User.objects.filter(phone=attrs["phone"]).exists()
        if phone_exists:
            raise ValidationError({"message": "Phone has already been used"})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data['role'] = 'employee'
        manager_user = self.context['request'].user
        user = User.objects.create_user(**validated_data, password=password)
        manager = Manager.objects.get(user=manager_user)
        Employee.objects.create(user=user, manager=manager)
        return user


# Profile Data Manager
class UserManagerProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "email", "first_name", "last_name", "phone", 'role']


# Profile Data Employee
class EmployeeSerializerProfile(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "email", "first_name", "last_name",
                  "phone", 'role', 'status', 'shift_time', 'date_hired']


# Update Profile Manager
class UpdateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone"]

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')
        if self.instance is not None:
            if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise serializers.ValidationError(
                    {"message": "This email is already in use."})
            if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
                raise serializers.ValidationError(
                    {"message": "This phone number is already in use."})
        return attrs

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance


# Update Profile Manager
class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name",
                  "phone", 'status', 'shift_time', 'date_hired']

    def validate(self, attrs, pk=None):
        email = attrs.get('email')
        phone = attrs.get('phone')
        if self.instance is not None:
            if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
                raise serializers.ValidationError(
                    {"message": "This email is already in use."})
            if User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
                raise serializers.ValidationError(
                    {"message": "This phone number is already in use."})
        return attrs

    def update(self, instance, validated_data):
        instance.__dict__.update(**validated_data)
        instance.save()
        return instance

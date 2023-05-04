from rest_framework import serializers
from .models import Report


class AddReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['text', 'product']

    def validate(self, data):
        if not data.get('text'):
            raise serializers.ValidationError(
                {"message": "Description of report is required."})
        if not data.get('product'):
            raise serializers.ValidationError(
                {"message": "Product is required."})

        # Check for empty values
        if data['text'] == '' or data['product'] == '':
            raise serializers.ValidationError(
                {"message": "Fields cannot be empty."})

        return data

    def create(self, validated_data):
        return super().create(validated_data)


class ReportSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField()
    product = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = ['id', 'text', 'added_by', 'product', 'created', 'updated']

    def get_added_by(self, obj):
        return f'{obj.added_by.first_name} {obj.added_by.last_name}'


class UpdateReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['text']
        read_only_fields = ['user']

    def validate(self, data):
        if not data.get('text'):
            raise serializers.ValidationError(
                {"message": "Description of report is required."})

        # Check for empty values
        if data['text'] == '':
            raise serializers.ValidationError(
                {"message": "Fields cannot be empty."})
        return data

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance

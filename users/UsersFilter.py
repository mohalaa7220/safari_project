from django_filters import rest_framework as filters
from .models import User
from django.db.models import Q


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_by_name')
    shift_time = filters.CharFilter(
        field_name='shift_time', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['name', 'shift_time']

    def filter_by_name(self, queryset, name, *args, **kwargs):
        return queryset.filter(
            Q(first_name__icontains=name) | Q(last_name__icontains=name)
        )

    def filter_queryset(self, queryset):
        name = self.request.query_params.get('name')
        if name:
            name_parts = name.split()
            if len(name_parts) == 1:
                queryset = self.filter_by_name(queryset, name_parts[0])
            elif len(name_parts) > 1:
                queryset = queryset.filter(
                    Q(first_name__icontains=name_parts[0]) & Q(
                        last_name__icontains=name_parts[-1])
                )
        return queryset

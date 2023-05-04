from django_filters import rest_framework as filters
from .models import User
from django.db.models import Q


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(method='filter_by_name')

    class Meta:
        model = User
        fields = ['name']

    def filter_by_name(self, queryset, name, *args, **kwargs):
        return queryset.filter(
            Q(first_name__icontains=name) | Q(last_name__icontains=name)
        )

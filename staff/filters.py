import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter

from store.models import *

class OrderFilter(django_filters.FilterSet):
    orderId = NumberFilter(field_name='id', lookup_expr='icontains')
    start_dateg = DateFilter(field_name='date_ordered', lookup_expr='gte')
    start_datel = DateFilter(field_name='date_ordered', lookup_expr='lte')
    class Meta:
        model = Order
        fields = [
            'customer',
            'status'
        ]

class OrderFilterC(django_filters.FilterSet):
    orderId = NumberFilter(field_name='id', lookup_expr='icontains')
    start_dateg = DateFilter(field_name='date_ordered', lookup_expr='gte')
    start_datel = DateFilter(field_name='date_ordered', lookup_expr='lte')
    class Meta:
        model = Order
        fields = [
            'status',
        ]


class ItemFilter(django_filters.FilterSet):
    product = django_filters.ModelChoiceFilter(queryset=Product.objects.all())
    class Meta:
        model = OrderItem
        fields = [
            'product'
        ]

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'tag'
        ]
     
class SearchRegistered(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email'
        ]

class SearchGuest(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email'
        ]
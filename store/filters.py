import django_filters
from django import forms

from .models import *

class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'tag'
        ]
     
class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = [
            'name',
            'tag'
        ]
     
class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = [
            'name',
            'category'
        ]

class SearchTag(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Tag
        fields = [
            'name',
        ]

class SearchCat(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Category
        fields = [
            'name',
        ]


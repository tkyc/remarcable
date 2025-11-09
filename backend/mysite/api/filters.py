import django_filters


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ProductFilter(django_filters.FilterSet):
    category = NumberInFilter(field_name='categories__id', lookup_expr='in')
    tag = NumberInFilter(field_name='tags__id', lookup_expr='in')

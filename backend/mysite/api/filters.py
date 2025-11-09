import django_filters


# Custom filter that combines NumberFilter with BaseInFilter functionality
# This allows filtering for multiple numeric values using "in" lookup
class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


# FilterSet for Product model with custom filtering capabilities
class ProductFilter(django_filters.FilterSet):
    # Filter by multiple category IDs using "in" lookup
    # Example: /products/?category=1,2,3 will return products in categories 1, 2, or 3
    category = NumberInFilter(field_name='categories__id', lookup_expr='in')
    
    # Filter by multiple tag IDs using "in" lookup  
    # Example: /products/?tag=4,5,6 will return products with tags 4, 5, or 6
    tag = NumberInFilter(field_name='tags__id', lookup_expr='in')

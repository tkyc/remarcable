from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .serializers import ProductSerializer, CategorySerializer, TagSerializer
from .models import Product, Category, Tag


class ProductListAPIView(generics.ListAPIView):
    """
    API endpoint that allows products to be viewed, searched and filtered.
    
    Supports:
    - Search: Case-insensitive search across product descriptions
    - Filtering: By categories and tags using ID lists
    - Distinct results: Prevents duplicates from many-to-many relationships
    """
    queryset = Product.objects.all().distinct()  # Distinct to avoid duplicates from joins
    serializer_class = ProductSerializer  # Serializer for converting Product objects to JSON
    filterset_class = ProductFilter  # Custom filter class for category/tag filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # Backends for filtering and search
    search_fields = ['description']  # Fields to search in (only description in this case)


class CategoryListAPIView(generics.ListAPIView):
    """
    API endpoint that returns all categories.
    
    Simple list view without search or filtering.
    Used for populating category dropdowns in frontend.
    """
    queryset = Category.objects.all()  # Get all category objects
    serializer_class = CategorySerializer  # Serializer for converting Category objects to JSON


class TagListAPIView(generics.ListAPIView):
    """
    API endpoint that returns all tags.
    
    Simple list view without search or filtering.
    Used for populating tag dropdowns in frontend.
    """
    queryset = Tag.objects.all()  # Get all tag objects
    serializer_class = TagSerializer  # Serializer for converting Tag objects to JSON

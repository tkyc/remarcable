from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .serializers import ProductSerializer, CategorySerializer, TagSerializer
from .models import Product, Category, Tag


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().distinct()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['description']


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

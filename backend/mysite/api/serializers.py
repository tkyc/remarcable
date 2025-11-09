from rest_framework import serializers
from .models import Product, Category, Tag


# Serializer for Category model - converts Category instances to/from JSON
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  # Specifies the Django model this serializer is based on
        fields = ['id', 'name']  # Includes only the id and name fields in serialized output


# Serializer for Tag model - converts Tag instances to/from JSON
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag  # Specifies the Django model this serializer is based on
        fields = ['id', 'name']  # Includes only the id and name fields in serialized output


# Product serializer with nested relationships
class ProductSerializer(serializers.ModelSerializer):
    # Nested serializers for related categories - displays full category objects
    categories = CategorySerializer(many=True, read_only=True)
    # Nested serializers for related tags - displays full tag objects
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product  # Specifies the Django model this serializer is based on
        fields = [
            'id',           # Product primary key
            'name',         # Product name
            'description',  # Product description
            'price',        # Product price
            'stock',        # Current stock quantity
            'categories',   # Related categories (nested serialization)
            'tags'          # Related tags (nested serialization)
        ]
        # Note: stocked_at field is excluded from the serialized output

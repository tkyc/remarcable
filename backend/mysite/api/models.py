from django.db import models


# Main product model representing items in the inventory
class Product(models.Model):
    name = models.CharField(max_length=80)  # Product name with maximum 80 characters
    description = models.TextField(blank=True)  # Optional detailed description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price with 2 decimal places precision
    stock = models.IntegerField(default=0)  # Current inventory count, defaults to 0
    stocked_at = models.DateTimeField(auto_now_add=True)  # Auto-set timestamp when product is added/updated

    def __str__(self):
        return f'{self.name}'  # String representation for admin and debugging

    class Meta:
        ordering = ['-stocked_at']  # Default ordering: most recently stocked products first


# Category model for organizing products into groups
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)  # Unique category name
    # Many-to-many relationship with Product through intermediate model ProductCategory
    product = models.ManyToManyField(Product, through='ProductCategory', related_name='categories')

    def __str__(self):
        return f'{self.name}'  # String representation returns category name

    class Meta:
        ordering = ['name']  # Default ordering: alphabetical by name


# Tag model for labeling products with keywords
class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)  # Unique tag name
    # Many-to-many relationship with Product through intermediate model ProductTag
    product = models.ManyToManyField(Product, through='ProductTag', related_name='tags')

    def __str__(self):
        return f'{self.name}'  # String representation returns tag name

    class Meta:
        ordering = ['name']  # Default ordering: alphabetical by name


# Intermediate model for Product-Category many-to-many relationship
class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Reference to Product
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Reference to Category

    class Meta:
        unique_together = ('product', 'category')  # Ensures a product can't be in the same category twice


# Intermediate model for Product-Tag many-to-many relationship
class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Reference to Product
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Reference to Tag

    class Meta:
        unique_together = ('product', 'tag')  # Ensures a product can't have the same tag twice

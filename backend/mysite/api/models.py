from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    stocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-stocked_at']


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    product = models.ManyToManyField(Product, through='ProductCategory', related_name='categories')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    product = models.ManyToManyField(Product, through='ProductTag', related_name='tags')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'category')


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'tag')

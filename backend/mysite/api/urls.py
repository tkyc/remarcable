from django.urls import path
from .import views 


urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='products_list'),
    path('categories/', views.CategoryListAPIView.as_view(), name='categories_list'),
    path('tags/', views.TagListAPIView.as_view(), name='tags_list'),
]

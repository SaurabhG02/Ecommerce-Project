from django.contrib import admin
from django.urls import path,include
from products.views import ProductListView,ProductDetailView, ProductFeaturedDetailView, ProductFeaturedListView
from .import views
urlpatterns = [
    path('',views.home, name='home' ),
    path('contact/',views.contact, name='contact' ),
    path('login/',views.login_page, name='login' ),
    path('register/',views.register_page, name='register' ),
    path('products/',ProductListView.as_view() ),
    path('featured/',ProductFeaturedListView.as_view(), name='featured-list' ),
    path('detail/<slug:slug>',ProductDetailView.as_view(), name='product-detail' ),
    path('featured/<slug:slug>',ProductFeaturedDetailView.as_view(), name='featured-detail' ),
]

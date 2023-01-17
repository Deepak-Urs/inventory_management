from django.urls import path

from product import views

urlpatterns = [
    path('products-list/', views.ProductsList.as_view())
]
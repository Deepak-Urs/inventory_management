from django.urls import path

from product import views

urlpatterns = [
    path('process_order', views.process_order),
    path('products-list/', views.ProductsList.as_view()),
    path('ship-package', views.shipPackage)
]
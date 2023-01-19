from django.urls import path

from product import views

urlpatterns = [
    #path('process_order/', views.ProcessOrder.as_view()),
    path('process_order', views.process_order),
    path('products-list/', views.ProductsList.as_view()) 
    #follow naming as init_catloag
]
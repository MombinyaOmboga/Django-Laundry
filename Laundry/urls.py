from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.landing, name='landing'),
    path('add-service/', views.add_service, name='add-service'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('about/', views.about, name='about'), 
    path('add-services-to-cart/', views.add_services_to_cart, name='add-services-to-cart'),
    path('delete-service-from-cart/<int:pk>/', views.delete_service_from_cart, name='delete-service-from-cart')
]
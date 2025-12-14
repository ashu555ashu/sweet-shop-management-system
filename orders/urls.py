from django.urls import path
from . import views

urlpatterns = [
    path('place/', views.place_order, name='place_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
]

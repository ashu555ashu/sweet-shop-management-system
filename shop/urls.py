from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from sweets.views import SweetViewSet
app_name = 'shop'


router = DefaultRouter()
router.register(r'sweets', SweetViewSet, basename='sweet')
urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('myshop/', views.my_shop, name='myshop'),
    path('api/', include(router.urls)),
    
]
router = DefaultRouter()
router.register(r'sweets', SweetViewSet, basename='sweet')

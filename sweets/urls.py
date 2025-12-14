from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from sweets.views import SweetViewSet

app_name = 'sweet'

router = DefaultRouter()
router.register(r'sweets', SweetViewSet, basename='sweet')

urlpatterns = [
    # =======================
    # Template-based Views
    # =======================
    path('list/', views.sweet_list_view, name='list'),
    path('add/', views.add_edit_sweet_view, name='add_sweet'),
    path('<int:sweet_id>/delete/', views.delete_sweet_view, name='delete_sweet'),
    path('<int:sweet_id>/restock/', views.restock_sweet_view, name='restock_sweet'),
    path('edit/<int:sweet_id>/', views.add_edit_sweet_view, name='edit_sweet'),

    # =======================
    # DRF Router
    # =======================
    path('api/', include(router.urls)),         

    # =======================
    # API Views
    # =======================
    path('api/sweets/', views.SweetListAPI.as_view(), name='sweet-list'),
    path('api/sweets/search/', views.SweetSearchAPI.as_view(), name='sweet-search'),
    path('api/sweets/add/', views.SweetCreateAPI.as_view(), name='sweet-add'),
    path('api/sweets/<int:pk>/', views.SweetUpdateAPI.as_view(), name='sweet-update'),
    path('api/sweets/<int:pk>/delete/', views.SweetDeleteAPI.as_view(), name='sweet-delete'),
    path('api/sweets/<int:pk>/purchase/', views.SweetPurchaseAPI.as_view(), name='sweet-purchase'),
    path('api/sweets/<int:pk>/restock/', views.SweetRestockAPI.as_view(), name='sweet-restock'),
]

from django.urls import path
from . import views
from .views import RegisterAPI, LoginAPI

app_name = 'accounts'

urlpatterns = [
    # Web views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Staff management (superuser only)
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/remove/<int:user_id>/', views.remove_staff, name='remove_staff'),

    # API endpoints
    path('api/auth/register/', RegisterAPI.as_view(), name='api_register'),
    path('api/auth/login/', LoginAPI.as_view(), name='api_login'),
]

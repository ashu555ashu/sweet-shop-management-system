from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
import sweetshop.settings as settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Redirect root URL to login
def redirect_to_login(request):
    return redirect('accounts:login')

urlpatterns = [
    path('', redirect_to_login),    
    # JWT APIs
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Django admin
    path('admin/', admin.site.urls),

    # Apps
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('sweet/', include('sweets.urls', namespace='sweet')),
    path('shop/', include('sweets.urls', namespace='sweet')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

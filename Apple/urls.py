from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Apple import settings
from shop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('api/categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('api/all/items/', PaginationItemsViewSet.as_view({'get': 'list'})),
    path('api/items/', ItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/items/<int:pk>/', ItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('shop.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound

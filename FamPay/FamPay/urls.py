from django.contrib import admin
from django.urls import path, include
from .views import schema_view, search_view

urlpatterns = [
    path('', search_view, name='video-search'),

    # Include DRF-Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/', include('FamPay_Task.urls'))
]

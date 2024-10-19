from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, VideoListView, APIKeyViewSet, call_function_view

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'api_key', APIKeyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('test/', call_function_view, name='call_function'),
]

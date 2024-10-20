from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, VideoListView, APIKeyViewSet, test_get_new_videos_periodic
# , video_list_view

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'api_key', APIKeyViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('test/', test_get_new_videos_periodic, name='call_function')
]

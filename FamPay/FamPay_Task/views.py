from rest_framework import viewsets
from .models import APIKey, Item, Video
from .serializers import APIKeySerializer, ItemSerializer, VideoSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer

class VideoPagination(PageNumberPagination):
    page_size = 10

class VideoListView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

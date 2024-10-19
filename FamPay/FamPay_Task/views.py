from django.http import HttpResponse
from rest_framework import viewsets
from .models import APIKey, Item, Video
from .serializers import APIKeySerializer, ItemSerializer, VideoSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import render
from .get_videos import *
import os
from dotenv import load_dotenv
load_dotenv()

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer

class VideoPagination(PageNumberPagination):
    page_size = 3

class VideoListView(ListAPIView):
    # queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = VideoPagination
    def get_queryset(self):
        queryset = Video.objects.all()
        query = self.request.query_params.get('query', None)

        if query:
            if query == "" or SearchQuery.objects.filter(query__icontains=query).exists():
                queryset = queryset.filter(title__icontains=query)
            else:
                print(f"Searching for a new query: {query}")
                get_new_videos_querywise(query)
                queryset = queryset.filter(title__icontains=query)

        return queryset

# Render to template
# def video_list_view(request):
#     videos = Video.objects.all()
#     return render(request, 'videos_list.html', {'videos': videos})

def test_get_new_videos_periodic(request):
    # result = get_new_videos_periodsic()  
    a = get_new_videos_querywise("fruit")
    return HttpResponse(a)


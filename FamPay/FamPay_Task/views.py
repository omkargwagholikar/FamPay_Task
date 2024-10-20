import os

from django.http import HttpResponse
from django.shortcuts import render
from dotenv import load_dotenv
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .get_videos import *
from .models import APIKey, Item, Video
from .serializers import APIKeySerializer, ItemSerializer, VideoSerializer

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
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

    def get_queryset(self):
        queryset = Video.objects.all()
        query = self.request.query_params.get("query", None)

        if query:
            if query == "" or query == os.getenv("video_search_query"):
                queryset = queryset.filter(title__icontains=query)
            else:
                print(f"Searching for a new query: {query}")
                get_new_videos_querywise(query)
                queryset = queryset.filter(title__icontains=query)

        return queryset


def test_get_new_videos_periodic(request):
    # result = get_new_videos_periodsic()
    a = get_new_videos_querywise("fruit")
    return HttpResponse(a)

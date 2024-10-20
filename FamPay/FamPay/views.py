from http.client import HTTPResponse
from django.shortcuts import render
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# This is purely for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="REST APIs",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def search_view(request):
    context = {
        'query': "",
        'videos': [],
        'page_obj': None,
    }
    return render(request, 'search.html', context)

def health_check(request):     
    return HTTPResponse({"message": "Pong!"})

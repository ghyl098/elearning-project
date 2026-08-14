from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


def home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Home page
    path('', home_view, name='home'),

    # Website URLs
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),

    # REST API
    path('api/', include('api.urls')),

    # OpenAPI schema
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    # Swagger UI
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    # ReDoc
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
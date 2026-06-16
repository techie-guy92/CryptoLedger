"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.db import connection
from django.db.utils import OperationalError


# def health_check(request):
#     try:
#         connection.ensure_connection()
#         return JsonResponse({
#             "status": "healthy",
#             "database": "connected"
#         })
#     except OperationalError:
#         return JsonResponse(
#             {
#                 "status": "unhealthy",
#                 "database": "disconnected"
#             },
#             status=503
#         )


def live_check(request):
    """
    Is Django process alive?
    """
    return JsonResponse({
        "status": "alive"
    })


def ready_check(request):
    """
    Can this pod serve traffic?
    """
    try:
        connection.ensure_connection()
        return JsonResponse({
            "status": "ready",
            "database": "connected"
        })
    except OperationalError:
        return JsonResponse(
            {
                "status": "not ready",
                "database": "disconnected"
            },
            status=503
        )


urlpatterns = [
    # path('health/', health_check, name='health-check'),
    path("health/live/", live_check, name="live-check"),
    path("health/ready/", ready_check, name="ready-check"),
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('users/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path("api-schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api-documents/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_title = 'CryptoLedger'
admin.site.index_title = 'CryptoLedger'
admin.site.site_header = 'CryptoLedger Administration'

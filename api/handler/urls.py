
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers,permissions
from application.views import AppIdViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
router = routers.DefaultRouter()
router.register(r'app-names',AppIdViewSet, basename='app_id' )

schema_view = get_schema_view(
    openapi.Info(
        title="Playstore API",
        default_version='1.0.0',
        description="API for managing Playstore app names",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('application.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

from django.urls import path, include
from .views import AppIdViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'app-names',AppIdViewSet, basename='app_id')
urlpatterns = [
    path('', include(router.urls))
]

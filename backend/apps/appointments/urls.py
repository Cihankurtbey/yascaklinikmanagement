from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, AppointmentSettingsViewSet

router = DefaultRouter()
router.register(r'', AppointmentViewSet, basename='appointment')
router.register(r'settings', AppointmentSettingsViewSet, basename='appointment-settings')

urlpatterns = [
    path('', include(router.urls)),
]

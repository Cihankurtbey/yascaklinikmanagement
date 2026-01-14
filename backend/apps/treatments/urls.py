from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreatmentViewSet, TreatmentTypeViewSet, OdontogramViewSet

router = DefaultRouter()
router.register(r'types', TreatmentTypeViewSet, basename='treatment-type')
router.register(r'', TreatmentViewSet, basename='treatment')
router.register(r'odontogram', OdontogramViewSet, basename='odontogram')

urlpatterns = [
    path('', include(router.urls)),
]

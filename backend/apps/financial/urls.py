from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PriceListViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'pricelist', PriceListViewSet, basename='pricelist')

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework.routers import DefaultRouter
from .views import AddressViewSet, TransactionViewSet

router = DefaultRouter()

router.register(r'addresses', AddressViewSet, basename='addresses')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from .views import AddressViewSet, ProfileViewSet, TransactionViewSet

router = DefaultRouter()

router.register(r'addresses', AddressViewSet, basename='addresses')
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls

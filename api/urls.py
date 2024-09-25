from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import (
    LoanTypeSet,
    LoanViewSet,
    PaymentViewSet,
)

router = DefaultRouter()
router.register(r'loans/types', LoanTypeSet)
router.register(r'loans', LoanViewSet)
router.register(r'payments', PaymentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
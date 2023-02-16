from django.urls import path, include
from users.views import UsersViewSet, SignupViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = routers.DefaultRouter()

router.register(r'users', UsersViewSet)

urlpatterns = [
    path(
        'auth/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'auth/token/refresh/', TokenRefreshView.as_view(),
        name='token_refresh'),
    path(
        'auth/token/verify/', TokenVerifyView.as_view(),
        name='token_verify'),
    path(
        'auth/signup/', SignupViewSet.as_view({'get': 'list'}),
        name='signup'),
    path('', include(router.urls))
]

from django.urls import path, include
from users.views import UsersViewSet, SignupViewSet, get_token
from rest_framework import routers

app_name = 'users'

router = routers.SimpleRouter()

router.register(r'users', UsersViewSet)

urlpatterns = [
    path(
        'auth/signup/', SignupViewSet.as_view({'post': 'create'}),
        name='signup'),
    path(
        'auth/token/', get_token, name='token'),
    path('', include(router.urls))
]

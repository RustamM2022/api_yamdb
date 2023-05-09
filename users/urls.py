from django.urls import include, path
from rest_framework import routers
from users.views import SignupViewSet, UsersViewSet, get_token

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

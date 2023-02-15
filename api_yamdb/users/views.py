from rest_framework import viewsets
from users.models import User
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    UserSerializer, UserCreateSerializer)
from rest_framework import filters
from .pagination import PostPagination
from rest_framework import status
from rest_framework import permissions
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


class UsersViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    lookup_field = 'username'
    pagination_class = PostPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']


@action(
    methods=['get', 'patch'],
    url_path='me',
    detail=False)
def user_profile(self, request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PATCH':
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignupViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserSerializer(request.user)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_create(**serializer.validated_data)
        confirmation_token = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения {confirmation_token}',
            from_email=None,
            recipient_list=(user.email,),
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import viewsets
from .permissions import IsSuperUserOrIsAdminOnly
from users.models import User
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import (
    UserSerializer, UserMeSerializer, SignupSerializer, TokenSerializer)
from rest_framework import filters
from .pagination import PostPagination
from rest_framework import status
from rest_framework import permissions
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken


class UsersViewSet(
    viewsets.ModelViewSet
):
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrIsAdminOnly,)
    lookup_field = 'username'
    pagination_class = PostPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']

    @action(
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
        detail=False)
    def user_profile(self, request):
        if request.method == 'GET':
            serializer = UserMeSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            user, created = User.objects.get_or_create(
                username=request.data.get('username'))
            confirmation_code = default_token_generator.make_token(user)
            user.confirmation_code = confirmation_code
            send_mail(
                subject='Код подтверждения',
                message=f'Ваш код подтверждения {confirmation_code}',
                from_email=None,
                recipient_list=(user.email,),
                fail_silently=False
            )
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=request.data.get('username'),
                                email=request.data.get('email'))
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code

        send_mail(
            subject='Код подтверждения',
            message=f'Ваш код подтверждения {confirmation_code}',
            from_email=None,
            recipient_list=(user.email,),
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = User.objects.get(username=serializer.validated_data['username'])
    except User.DoesNotExist:
        return Response({'username': 'нет такого пользователя'},
                        status=status.HTTP_404_NOT_FOUND)
    if not default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']):
        return Response(
            "Confirmation_token недействителен.",
            status=status.HTTP_400_BAD_REQUEST)
    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)}, status=status.HTTP_200_OK)

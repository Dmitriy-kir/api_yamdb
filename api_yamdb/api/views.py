import os
import sys
from datetime import datetime

from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from reviews.models import Categories, Genres, Reviews, Titles
from users.models import User

from .pagination import CustomPagination
from .permissions import (IsAdminOrReadOnlyPermission,
                          IsAuthenticatedOrReadOnly,
                          IsAuthorOrModeratorOrReadOnlyPermission,
                          IsSuperUserOrAdminPermission)
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, RegistrationSerializer,
                          ReviewsSerializer, TitlesGetSerializer,
                          TitlesPostSerializer, TokenSerializer,
                          UserMySelfSerializer, UserSerializer)

sys.path.append(os.path.abspath('..'))


class SignupViewSet(APIView):

    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            data['email_subject'],
            data['email_body'],
            data['to_email'],
            fail_silently=False
        )
        email.send()

    @staticmethod
    def period_of_time():

        now = str(datetime.datetime.now())
        if 0 < now.hour <= 6:
            return 'Доброй ночи'
        elif 6 < now.hour <= 12:
            return 'Доброе утро'
        elif 12 < now.hour <= 18:
            return 'Добрый день'
        return 'Добрый вечер'

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        time = self.period_of_time()
        email_body = (
            f'{time}, {user.username}!'
            f'\nКод подтвержения для доступа к API:'
            f' {user.confirmation_code}'
            f'Наберите его в поле ввода.'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenViewSet(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        data = serializer.data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = TokenObtainPairSerializer().get_token(request.user)
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )
        return Response(
            'Неверный код :(',
            status=status.HTTP_400_BAD_REQUEST
        )


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesPostSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('genre', 'category', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesGetSerializer
        return TitlesPostSerializer


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Материский ViewSet для создания, просмотра  и удаления списка объектов,
       используется во всех ViewSet с ограниченным функционалом"""
    pass


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrModeratorOrReadOnlyPermission,)

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrModeratorOrReadOnlyPermission,)

    def get_queryset(self):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrAdminPermission,)
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticatedOrReadOnly,),
        url_path='me'
    )
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin or request.user.is_superuser:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserMySelfSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)

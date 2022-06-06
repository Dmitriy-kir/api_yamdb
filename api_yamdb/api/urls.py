from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, SignupViewSet, TitlesViewSet, TokenViewSet,
                    UsersViewSet)

app_name = 'api'

router = SimpleRouter()

router.register(
    r'auth/signup/',
    SignupViewSet, basename='signup'
)
router.register(
    r'auth/token/',
    TokenViewSet, basename='token'
)
router.register(
    r'titles',
    TitlesViewSet, basename='titles'
)
router.register(
    r'categories',
    CategoriesViewSet, basename='categories'
)
router.register(
    r'genres',
    GenresViewSet, basename='genres'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet, basename='comments',
)
router.register(
    'users',
    UsersViewSet, basename='users'
)
urlpatterns = [
    path('v1/', include(router.urls)),
]

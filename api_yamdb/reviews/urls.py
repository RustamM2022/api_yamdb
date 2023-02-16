from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet 

app_name = 'reviews'

router = DefaultRouter()

router.register(
    r'titles/(?P<title.id>\d+)/reviews/(?P<review.id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles/(?P<title.id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
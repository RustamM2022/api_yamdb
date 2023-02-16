from django.urls import include, path
from rest_framework import routers

from reviews.views import (CommentViewSet, ReviewViewSet)

app_name = 'api'

router = routers.DefaultRouter()


router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'^titles/(?P<title _id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]

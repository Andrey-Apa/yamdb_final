from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, UserCreateViewSet, CategoryViewSet,
                    GenreViewSet, CustomTokenObtain, TitleViewSet,
                    ReviewViewSet, CommentViewSet)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='user')
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet.as_view()),
    path('v1/auth/token/', CustomTokenObtain.as_view()),
    path('v1/', include(v1_router.urls)),
]

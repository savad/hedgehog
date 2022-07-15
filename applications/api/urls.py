from django.urls import path, include

from rest_framework.routers import DefaultRouter

from applications.api import views


router = DefaultRouter()
router.register(r'register', views.CreateUserViewSet, basename='register')
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'follow', views.FollowViewSet, basename='follow')

router.register(r'image-list', views.ImageViewSet, basename='image')
router.register(r'image-upload', views.ImageUploadViewSet, basename='image-upload')
router.register(r'images-for-user-feed', views.UserImageViewSet, basename='image-feed-for-user')
router.register(r'like', views.LikesViewSet, basename='like')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/login/', views.LoginView.as_view(), name='login'),
]

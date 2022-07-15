from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from applications.api.serializers import ImageSerializer, FollowSerializer, LoginSerializer,\
    CreateUserSerializer, UserSerializer, LikeSerializer
from applications.images.models import Image
from applications.followers.models import Follow
from applications.accounts.models import User
from applications.likes.models import Like


class LoginView(APIView):
    """
    Views for a user to login
    @param: username:str required
    @param: password:str required
    @return: dict: status: str, token:str, username:str
    """
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if user:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'status': 'success', 'username': serializer.data['username'], "token": token.key})
            else:
                return Response({'status': 'error', 'message': 'User is inactive'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'message': 'Invalid credential'}, status=status.HTTP_400_BAD_REQUEST)


class CreateUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for register a new user
    @:param: username:str required
    @:param: password:str required
    @:param: home_town:str non-required
    @:param: phone_number:str non-required
    @:param: profile_description:str non-required
    @:return: user info dict
    """
    http_method_names = ['post', ]
    permission_classes = (AllowAny, )
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        """
        Override 'perform_create' to save password in the encrypted formate
        """
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserViewSet(viewsets.ModelViewSet):
    """
    Views for listing all the users
    @:param
    @:return: list of users
    """
    http_method_names = ['get', ]
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ImageViewSet(viewsets.ModelViewSet):
    """
    Views for listing all the images, sorted by likes count
    @:param
    @:return: list of image feeds
    """
    http_method_names = ['get', ]
    permission_classes = (AllowAny, )
    serializer_class = ImageSerializer
    queryset = Image.objects.all().order_by('-likes')


class UserImageViewSet(ImageViewSet):
    """
    Views for listing follower images sorted by recent
    @:param
    @:return: list of images
    """
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        following_users = Follow.objects.filter(follower=self.request.user).values_list('following')
        return self.queryset.filter(user__in=following_users).order_by('-created')


class ImageUploadViewSet(ImageViewSet):
    """
    Views for upload or delete an image
    @:param image:image-file required
    @:param image_caption:str required
    @:return: dict: image-info
    """
    http_method_names = ['post', 'delete']
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @swagger_auto_schema(request_body=ImageSerializer)
    def perform_create(self, serializer):
        """
        Override to add user to serializer
        """
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """
    View Set to change the status to follow or un-follow as per the request.
    @:param following:int user-id required
    @:return: dict: follow-info
    """
    permission_classes = (IsAuthenticated, )
    http_method_names = ['post', 'delete']
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def get_queryset(self):
        return self.queryset.filter(follower=self.request.user)

    def perform_create(self, serializer):
        """
        Override to send follower to serializer
        """
        serializer.save(follower=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class LikesViewSet(viewsets.ModelViewSet):
    """
    View Set for like/undo-like an image feed
    @:param image:int image-id required
    @:return: dict: like-info
    """
    permission_classes = (IsAuthenticated, )
    http_method_names = ['post', 'delete']
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Override to send user to serializer
        """
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

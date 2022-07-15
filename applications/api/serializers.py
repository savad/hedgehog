from rest_framework import serializers
from rest_framework.serializers import ValidationError

from PIL import Image as StdImage
from drf_yasg import openapi

from applications.accounts.models import User
from applications.images.models import Image
from applications.followers.models import Follow
from applications.likes.models import Like


class LoginSerializer(serializers.Serializer):
    """
    Login serializer for validating login input data
    """
    username = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    Basic user serializer, it will serialize basic user information
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'followers_count', 'following_count')
        read_only_fields = ('followers_count', 'following_count')


class CreateUserSerializer(UserSerializer):
    """
    Serializer for validating user register input data
    """

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('password', 'home_town', 'phone_number', 'profile_description')
        read_only_fields = UserSerializer.Meta.read_only_fields + ('id', )
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}


class ImageSerializer(serializers.ModelSerializer):
    """
    Image serializer, it will serialize image model data
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'image', 'image_caption', 'created', 'user', 'likes']
        read_only_fields = ['id', 'created', 'image_caption', 'likes']
        swagger_schema_fields = {
            "properties": {
                "image": openapi.Schema(
                    title="image",
                    type=openapi.TYPE_FILE,
                ),
                "image_caption": openapi.Schema(
                    title="image_caption",
                    type=openapi.TYPE_STRING,
                ),
            },
            "required": ["image", "image_caption"],
        }

    def validate_image(self, value):
        try:
            StdImage.open(value).verify()
        except:
            raise ValidationError("Unsupported image file")
        return value


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer to follow and Un follow a user
    """
    follower_details = UserSerializer(source='follower', read_only=True)
    following_user_details = UserSerializer(source='following', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'following', 'follower', 'created', 'following_user_details', 'follower_details']
        read_only_fields = ['id', 'follower', 'following_user_details', 'follower_details', 'created']

    def validate_following(self, value):
        follow_count = Follow.objects.filter(follower=self.context['request'].user, following=value).count()
        if follow_count > 0:
            raise ValidationError("User already following")
        return value


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer to like and un-like an image feed
    """
    liked_user_details = UserSerializer(source='user', read_only=True)
    image_details = ImageSerializer(source='image', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'image', 'created', 'liked_user_details', 'image_details']
        read_only_fields = ['id', 'user', 'created', 'liked_user_details', 'image_details']

    def validate_image(self, value):
        follow_count = Like.objects.filter(user=self.context['request'].user, image=value).count()
        if follow_count > 0:
            raise ValidationError("User already liked")
        return value

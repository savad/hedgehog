from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from PIL import Image
from io import BytesIO

from applications.accounts.models import User
from applications.followers.models import Follow
from applications.images.models import Image as ImageModel
from applications.likes.models import Like

client = APIClient()


def create_image(size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    image_file = SimpleUploadedFile('avatar.png', data.getvalue())
    return image_file


class LoginViewTestCase(TestCase):
    token = None

    def setUp(self):
        self.base_url = reverse("login")
        user = User.objects.create(username="test@test.com", password="1234")
        user.set_password("1234")
        user.save()
        client.credentials()

    def test_login_endpoint(self):
        response = client.post(self.base_url, {"username": "test@test.com", "password": "1234"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")

    def test_login_with_invalid_data(self):
        response = client.post(self.base_url, {"username": "test@test.com", "password": "test"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "error")


class CreateUserViewSetTestCase(TestCase):
    def setUp(self):
        self.base_url = reverse("register-list")

    def test_create_endpoint(self):
        response = client.post(self.base_url, {"username": "newuser@test.com", "password": "1234"})
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data["id"], int)

    def test_create_endpoint_with_missing_username(self):
        response = client.post(self.base_url, {"name": "test@test.com", "password": "test"})
        self.assertEqual(response.status_code, 400)

    def test_create_endpoint_with_missing_password(self):
        response = client.post(self.base_url, {"username": "test@test.com"})
        self.assertEqual(response.status_code, 400)

    def test_create_endpoint_with_empty_body(self):
        response = client.post(self.base_url, {})
        self.assertEqual(response.status_code, 400)


class BaseUserAuthMixinTestCase(TestCase):

    def setUp(self):
        self.user = {"username": "token@test.com", "password": "1234"}
        client.post(reverse("register-list"), self.user)
        response = client.post(reverse("login"), self.user)
        self.token = response.data['token']


class UserViewSetTestCase(BaseUserAuthMixinTestCase):

    def test_user_list_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.get(reverse("users-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        client.credentials()

    def test_user_list_endpoint_without_valid_token(self):
        client.credentials()
        response = client.get(reverse("users-list"))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response.data, dict)


class ImageViewSetTestCase(BaseUserAuthMixinTestCase):

    def test_image_list_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        image_file = create_image()
        image_input = {"image": image_file, "image_caption": "Lorem Ipsum"}
        client.post(reverse("image-upload-list"), image_input)
        response = client.get(reverse("image-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertGreater(len(response.data), 0)
        client.credentials()

    def test_image_list_endpoint_without_valid_token(self):
        client.credentials()
        response = client.get(reverse("image-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)


class UserImageViewSetTestCase(BaseUserAuthMixinTestCase):

    def test_user_image_feed_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        image_file = create_image()
        image_input = {"image": image_file, "image_caption": "Lorem Ipsum"}
        client.post(reverse("image-upload-list"), image_input)
        response = client.get(reverse("image-feed-for-user-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        client.credentials()

    def test_user_image_feed_endpoint_without_valid_token(self):
        client.credentials()
        response = client.get(reverse("image-feed-for-user-list"))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response.data, dict)


class ImageUploadViewSetTestCase(BaseUserAuthMixinTestCase):

    def test_image_upload_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        image_file = create_image()
        image_input = {"image": image_file, "image_caption": "Lorem Ipsum"}
        response = client.post(reverse("image-upload-list"), image_input)
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data["id"], int)
        client.credentials()

    def test_image_upload_without_valid_token(self):
        client.credentials()
        image_file = create_image()
        image_input = {"image": image_file, "image_caption": "Lorem Ipsum"}
        response = client.post(reverse("image-upload-list"), image_input)
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response.data, dict)


class FollowViewSetTestCase(BaseUserAuthMixinTestCase):

    def setUp(self):
        super(FollowViewSetTestCase, self).setUp()
        self.following = User.objects.create(username="following@test.com", password="1234")

    def test_follow_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post(reverse("follow-list"), {"following": self.following.id})
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data["id"], int)
        client.credentials()

    def test_follow_without_valid_body_content(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post(reverse("follow-list"), {})
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response.data, dict)
        client.credentials()

    def test_follow_without_valid_token(self):
        client.credentials()
        response = client.post(reverse("follow-list"), {"following": self.following.id})
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response.data, dict)

    def test_unfollow_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        user = User.objects.get(username=self.user["username"])
        follow = Follow.objects.create(following=self.following, follower=user)
        response = client.delete(reverse("follow-detail", kwargs={'pk': follow.id}))
        self.assertEqual(response.status_code, 204)
        client.credentials()

    def test_unfollow_without_valid_token(self):
        client.credentials()
        user = User.objects.get(username=self.user["username"])
        follow = Follow.objects.create(following=self.following, follower=user)
        response = client.delete(reverse("follow-detail", kwargs={'pk': follow.id}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response.data, dict)


class LikesViewSetTestCase(BaseUserAuthMixinTestCase):

    def setUp(self):
        super(LikesViewSetTestCase, self).setUp()
        user = User.objects.get(username=self.user["username"])
        self.image_file = create_image()
        self.image = ImageModel.objects.create(image=self.image_file, image_caption="Lorem", user=user)

    def test_like_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post(reverse("like-list"), {"image": self.image.id})
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data["id"], int)
        client.credentials()

    def test_like_without_valid_body_content(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = client.post(reverse("like-list"), {})
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response.data, dict)
        client.credentials()

    def test_like_without_valid_token(self):
        client.credentials()
        response = client.post(reverse("like-list"), {"image": self.image.id})
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response.data, dict)

    def test_undo_like_endpoint(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        user = User.objects.get(username=self.user["username"])
        like = Like.objects.create(user=user, image=self.image)
        response = client.delete(reverse("like-detail", kwargs={'pk': like.id}))
        self.assertEqual(response.status_code, 204)
        client.credentials()

    def test_undo_like_without_valid_token(self):
        client.credentials()
        user = User.objects.get(username=self.user["username"])
        like = Like.objects.create(user=user, image=self.image)
        response = client.delete(reverse("like-detail", kwargs={'pk': like.id}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response.data, dict)

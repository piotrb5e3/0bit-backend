from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework_jwt import utils

from posts.models import Post
from posts.tests.factory import create_post


class TestPost(APITestCase):
    unpublish_url_name = 'post-unpublish'

    published_post = None

    auth_token = None
    auth = None

    def setUp(self):
        self.published_post = create_post()

        user = User.objects.create_user("username", "password1")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {0}'.format(self.auth_token)

    def test_can_unpublish_post_when_logged_in(self):
        url = reverse(self.unpublish_url_name, args=[self.published_post.id])
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self._assert_post_unpublished(self.published_post.id)

    def test_cant_unpublish_post_when_anonymous(self):
        url = reverse(self.unpublish_url_name, args=[self.published_post.id])
        response = self.client.post(url)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self._assert_post_published(self.published_post.id)

    def _assert_post_published(self, pk):
        posts = Post.objects.filter(pk=pk, published=True)
        self.assertEqual(1, len(posts))

    def _assert_post_unpublished(self, pk):
        posts = Post.objects.filter(pk=pk, published=False)
        self.assertEqual(1, len(posts))

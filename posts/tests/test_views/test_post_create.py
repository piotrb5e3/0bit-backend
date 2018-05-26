from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt import utils
from django.contrib.auth.models import User

from posts.models import Post

from posts.tests.factory import create_post, create_edited_post


class TestPost(APITestCase):
    list_url_name = 'post-list'
    detail_url_name = 'post-detail'
    test_title = "This is a random title"
    test_contents = "This is not a random text"
    test_post = {
        "title": test_title,
        "contents": test_contents
    }
    auth_token = None
    auth = None
    post0 = None
    post1 = None

    def setUp(self):
        self.post0 = create_post()
        self.post1 = create_edited_post()
        user = User.objects.create_user("username", "password1")
        payload = utils.jwt_payload_handler(user)
        self.auth_token = utils.jwt_encode_handler(payload)
        self.auth = 'JWT {0}'.format(self.auth_token)

    def test_cant_crete_new_post_when_anonymous(self):
        url = reverse(self.list_url_name)
        response = self.client.post(url, self.test_post)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(Post.objects.all()))

    def test_cant_crete_new_post_with_bad_token(self):
        url = reverse(self.list_url_name)
        auth = 'JWT {0}'.format("BAD" + self.auth_token)
        response = self.client.post(url, self.test_post,
                                    HTTP_AUTHORIZATION=auth)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual(2, len(Post.objects.all()))

    def test_can_crete_new_post_when_authenticated(self):
        url = reverse(self.list_url_name)
        response = self.client.post(url, self.test_post,
                                    HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, len(Post.objects.all()))
        self._assure_changes_successful()

    def _assure_changes_successful(self):
        post = Post.objects.filter(title=self.test_title)
        self.assertEqual(1, len(post))
        self.assertEqual(self.test_title, post[0].title)
        self.assertEqual(self.test_contents, post[0].contents)

    def _assert_unchanged_state(self):
        self.assertEqual(2, len(Post.objects.all()))
        self.assertEqual(0, len(Post.objects.filter(title=self.test_title)))
        self.assertEqual(
            0,
            Post.objects.filter(contents=self.test_contents).count()
        )
